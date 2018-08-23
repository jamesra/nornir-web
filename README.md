nornir-web
==========

This is a Python 3.x web service that services arbitrary volume-registered images to clients.  It works but was never fast enough for production use.


The vision at the time:
	One service per volume.
	The service imports/updates the volume at startup.  The key result was a  SQL database used to map regions in volume space to all intersecting transforms and raw images.
	The service accepted HTTP requests for arbitrary regions in volume space.  The response image is built by merging and cropping small volume registered non-overlapping tiles.  Tiles were loaded from disk.  Stale or missing tiles were calculated from section (aka slice) space images (GPU step) and saved to disk.
	Eventually I wanted the service to have a queue of tiles to build during idle times.  After the web service was active for a while it would generate registered images for the entire volume.  Then it would patrol for changes to the input data/transforms and auto-update the registered tiles.

What I liked:
	End-users getting arbitrary images.  It avoids clients needing to manipulate images and adjust coordinates.  Trivial for a service to get the image for an annotation.
	Updates to raw images/transforms are immediately visible to clients.  Heavily trafficked regions are quickly updated+cached.
Registered images eventually being on disk.

Problems:
	Import/Update was slow at startup. (If I could magically fix a past bad programming decision Nornir would use SQL and not XML for meta-data.)
	Long running processing jobs need updates to be versioned or prevented entirely.
When I was distracted away from the project I was working through performance issues.  The SQL queries were slow, hopefully solvable with a spatial database and partitioning the lookup structures by Z-level.  I also recall Python’s threading being a blocking issue as I flooded the server with dozens of requests from a Viking client.
