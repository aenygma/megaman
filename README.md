# megaman
megatools with a sweet, sexy backend
---
![Our Robotr0n and Sausages](megaman.png)

---

## Schematic

* megatools downloader - worker node
* api 
* history - database
* cli interface (CRUD)


## User stories

* Submit a url to download. 
 * Submit it to the queue
   * Validate url
    * Add attributes; proper name, path, etc
   * Check if already downloaded
 * Worker node in daemon mode, checks queue and downloads
  * 

 * General configs
  * Download time schedule
  * 

* Consumer / Daemon mode
 * gets entry from queue
 * prepares command line args
 * execs cli
 

* API / Interface 
 * Submit jobs
 * List jobs
 * Remove jobs
 * CRUD jobs

 * RESTful ?
 
 * CLI = client of API



