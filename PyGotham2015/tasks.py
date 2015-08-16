from celery import Celery, Task
import concurrent.futures
import requests
from yields import MyParser, ParSerializer

app = Celery('tasks', backend='amqp', broker='amqp://guest@localhost//', include=['parser'])

CELERY_RESULT_BACKEND = 'amqp'
CELERY_TASK_RESULT_EXPIRES = 18000

@app.task
def parse_doc(file_to_parse=None):

    my_parser = MyParser()

    # Parse an incoming file
    soup = my_parser.parse(file(file_to_parse))

    # Parse just the data from the beautifulsoup object
    bond_obj = my_parser.parseData(soup)

    return True


@app.task
def spot_bootstrap():

    strapper = Bootstrap()

    # Bootstrap
    strapper.boostrap()

    return True


@app.task
def file_downloader(urls):

    if urls is None or len(urls) == 0:
        return

    def load_url(url, timeout):
        session = requests.Session()
        session.mount("http://", requests.adapters.HTTPAdapter(max_retries=5))
        session.mount("https://", requests.adapters.HTTPAdapter(max_retries=5))

        request = session.get(url=url, stream=True, timeout=timeout)

        return request

    # We can use a with statement to ensure threads are cleaned up promptly
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Start the load operations and mark each future with its URL
        future_to_url = {executor.submit(load_url, url, 60): url for url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()

                if data.status_code == requests.codes.ok:

                    local_filename = url.split(' ')[2]
                    with open(local_filename, 'wb') as handle:
                        for block in data.iter_content(chunk_size=1024):
                            if not block:
                                break
                            handle.write(block)
                        handle.close()
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))
    return True
