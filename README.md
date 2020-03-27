## Background

The repertory is a collection of officials from medieval times until 1862 from supra-regional state  institutions of the Netherlands, containing 12,000 officials and many more of their positions in the old version that was published in 2009. After that much new information was added about the Republic period (1576-1796) and medieval times. We mainly need it for our REPUBLIC project, that is intended to publish all States General resolutions (decisions, about 1 million) from 1576-1796 online. To resolve all officials, the repertory is an invaluable aid. As the applications is outdated from both a technical and a content perspective, it should be updated. This project is to document this update and the porting to a new framework, documenting it as we go.

As there are separate databases for each period and within the republic period  subdivisions per province, these have to be joined before the database can be updated. There is a possible overlap between officials from one period to another, they have to be disambiguated. This was done previously; it is preferable to keep the old database and extend it with the additions, but this may prove to be difficult.

The old application was created in zope and mysqldbda, a precursor of sqlalchemy and meant to be an object-relational mapping. This is far outdated and has many problems, including problems with (being Python2) encoding. With sqlalchemy, the idea is that many of the object declaration could be retained and relatively easily ported. The structure of the database will kept as it is. Now, the application has a single interface for all periods. While this may be desirable in some case, making separate interfaces for different periods is preferable to make the search screens/boxes less cluttered. There will be many additional choices in this regards, but we will face them when the web interface is at order, much later in the process.

## Choices

* create new pipenv environment nw_raa (for new repertorium ambtenaren en ambtsdragers
* install flask,
