import time
import numpy as np
import click
from datetime import datetime

from ._cli_common import main
from odc.aws.queue import get_messages, get_queue


@main.command("mock-long-run")
@click.option(
    "--dryrun",
    is_flag=True,
    help="Do not run computation, from long execution test",
)
def mock_log_run(dryrun):
    """
       Mock long executing tasks
    """
    start_t = datetime.now()
    sqs_queue = get_queue('deafrica-prod-eks-stats-geomedian')
    for msg in get_messages(sqs_queue, visibility_timeout=1260):
        while (datetime.now() - start_t).total_seconds() < 1:
            wl1 = np.random.normal(0,1,(100000,10000))
            wl2 = np.random.normal(0,1,(100000,10000))
            Wl3 = wl1 * wl2
            msg.delete()

    s3 = boto3.resource('s3')
    object = s3.Object('deafrica-data', f'esa/s2/ga_s2_clear_pixel_count/0.0.1/test/{msg}.txt')
    object.put(Body=b'some data')
    print("DONE")

