# PiBox-Daemon

This is the daemon that will run in the background listening to folder changes

The Daemon needs to do 2 things 

1. Watch for changes locally and upload them to the server
2.  Watch for changes on the server and download them locally
    * Probably a cron-job-thing that syncs every X mins