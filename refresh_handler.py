"""Lambda entry point for the scheduled metadata refresh.

Point a second Lambda function at the same image this repo already builds
(see deploy.sh) with its handler set to `refresh_handler.handler`, then wire
an EventBridge scheduled rule (e.g. rate(1 day)) to invoke it. No API
Gateway/Function URL needed -- EventBridge calls the handler directly.
"""

from refresh_metadata import refresh_stale_videos


def handler(event, context):
    return refresh_stale_videos()
