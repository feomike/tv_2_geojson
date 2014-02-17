tv_2_geojson
============

takes a TV Study extract file from the FCC and writes out a geoJson file


This repo was made in order to transfer the [TV Extract File](http://www.fcc.gov/encyclopedia/tv-service-contour-data-points) from the FCC to a geoJson file.  The file found at the site above is a fixed field csv file.  It contains geographic data in the form of latitude and longitude points for the tower plus latitude and longitude points representing 1 degree marks (up to 360 degrees) from the tower for the FCC contour line representing the TV area.  Please read the full link above for all the engineering specifications about the tower and/or contour line.  

The advantage this repo has, is it very quickly transfers the relatively unusable csv file into a geographic dataset.  Furthermore, the codebase does not have any dependencies other than python.  It merely transfers the csv into the geoJson spec.  

Output
------
The resulting file outputs two geojson files; (1) one for the tower locations and (2) and one for the contour lines.  The full set of all attributes from the input csv are placed on both resulting geoJson file.

Issues
-----
- appID might not be unique.  no idea why this is;
- service has values of CA, DC, DD, DM, DN, DR, DS, DT, DX, LD, TV, TX; currently these values are not decoded;
- the call sign isn't being pulled cleanly out of the description.  it could use some work to get the clean call sign.  sometimes this is a 4 digit number, sometimes it is a 5 digit, sometimes it is a 4 + 2 digit w/ a '-' in between 
- rather than reading and writing lines, it might be better to read the file in as a csv file or an array and grab data elements out as array elements.to do this w/ python, one would use the genfromtxt command, but i struggled with it.  

Examples
--------
See the [Examples](examples) for some example output from this script.

License
-------
The project is a public domain work and is not subject to domestic or international copyright protection. See the [license]() file for additional information.

Members of the public and US government employees who wish to contribute are encourage to do so, but by contributing, dedicate their work to the public domain and waive all rights to their contribution under the terms of the [CC0 Public Domain Dedication](http://creativecommons.org/publicdomain/zero/1.0/).
