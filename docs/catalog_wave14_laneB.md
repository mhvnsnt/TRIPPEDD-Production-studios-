# TRIPPEDD Resource Pull Program — Wave 14, Lane B: Municipal / State Public-Domain Photo Archives

Lane: city, county, and state government photo archives, municipal open-data portals with imagery, state DOT image libraries, parks-department photo libraries, and international municipal equivalents. Every license status verified against the upstream rights page (see **License** line per entry). Verification date: 2026-10-07.

The municipal lane is the classic rights trap: a city archive being "public" does not make its photos public domain. US cities and states (unlike federal agencies) CAN and DO assert copyright. This wave documents both the genuinely free archives and the fee/permission traps, with 11 quarantine rows appended to docs/LICENSE_QUARANTINE.md.

---

## ✅ Verified commercial-safe

#### City of Boston Archives (Flickr) — City of Boston ✅
- **What:** The City of Boston Archives' official Flickr stream: thousands of scans of city engineering, public-works, school, and boundary-mark records (ca. 1896–1950s), each item carrying an explicit "Rights: Public Domain" field from the Archives itself.
- **URL:** https://flic.kr/photos/cityofbostonarchives/8368220058/ (example record — "Rights: Public Domain"; account: City of Boston Archives)
- **License:** Public Domain, per-item rights field on the Archives' official Flickr (verified 2026-10-07 via Flickr item page)
- **Free tier:** free download, no account (Flickr sizes); filter the photostream for the PD-marked items
- **Repo lane:** trippedd (backgrounds)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Boston street/infrastructure plates with unusual per-item PD clarity for a municipal archive — pull the PD-marked items only; confirm the "Rights" field per photo. [Wave 14 Lane B]

#### Florida Memory — State Library & Archives of Florida ✅
- **What:** Florida Memory Program: 320,000+ digitized photographs, documents, maps, plus film and audio from the State Archives of Florida — 206,000+ photos spanning mid-16th-century maps to present-day, including Cape Canaveral launches, Daytona speed runs, Miami street scenes, small towns.
- **URL:** https://www.dos.myflorida.com/library-archives/archives/florida-memory/ (rights: FL Stat. §257.35(6) — "Any use or reproduction of material deposited with the Florida Photographic Collection shall be allowed… provided that appropriate credit for its use is given"; Archives' 2008 statement to Wikipedia: "You may use any of the images posted on the Florida Memory Project website. The State Archives of Florida is not aware of any copyright issues with any of the images")
- **License:** Free to use with credit (Florida statute + State Archives statement; verified 2026-10-07)
- **Free tier:** free download, no account; bulk browsing by collection/decade
- **Repo lane:** trippedd (backgrounds)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Strongest state-level plate source in the wave — 20th-century Florida streets, beaches, motels, signage, rockets. Credit line required per statute ("Courtesy of the State Archives of Florida"); some holdings are from private collections with donation-agreement terms, so check per-item notes on post-1960 material. [Wave 14 Lane B]

#### City of Toronto Archives — municipal photo archive ✅
- **What:** Official repository of Toronto civic records: 1.25M+ photographs from 1856, plus 10,000+ maps and aerial photographs (1947–1992); Archives item records carry a "Copyright is in the public domain" field (e.g., the Alfred J. Pearson TTC streetcar series).
- **URL:** https://www.toronto.ca/city-government/accountability-operations-customer-service/access-city-information-or-records/city-of-toronto-archives/ (rights: per-item "Copyright is in the public domain and permission for use is not required" on Archives item records, via the Archives' database)
- **License:** Public Domain per item (Archives' own rights field; verified 2026-10-07 via item records)
- **Free tier:** free browsing, no account; searchable database
- **Repo lane:** trippedd (backgrounds)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Pre-amalgamation streetcar/street plates are the BG gold here. Caveat: the 1947–1992 aerial photographs are view-only (JPEG 2000, not downloadable) — reference only. Confirm the PD field per item; non-government fonds (families, businesses) may carry different rights. [Wave 14 Lane B]

#### MassGIS Aerial Imagery — Commonwealth of Massachusetts ✅
- **What:** MassGIS (Bureau of Geographic Information) statewide orthoimagery: 15-cm 2019 leaf-off color orthophotos, 2023 and 2025 vintages, plus older imagery back decades — Boston streets, harbors, suburbs, coastline at survey grade, served via tile services (WMTS) and bulk download.
- **URL:** https://www.mass.gov/info-details/massgis-data-2023-aerial-imagery (rights: MassGIS FAQ — "Since MassGIS data is paid for by public tax dollars, the data are in the public domain and therefore can be used by anyone for any purpose"; 2023 imagery page: "No restrictions apply to these data")
- **License:** Public Domain (verified via mass.gov FAQ + imagery page, 2026-10-07)
- **Free tier:** free download + WMTS tile services, no account; JPEG 2000 tiles (~19 MB each)
- **Repo lane:** trippedd (backgrounds)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Top-down plates for city-layout reference, matte-painting bases, and era aerials. Nuance: MassGIS confirmed the 2015 ortho layer's "imagery itself cannot be redistributed" page text was a publishing-system artifact — imagery is usable for any purpose including deriving data; prefer 2019+ vintages for clean redistribution. [Wave 14 Lane B]

#### Nationaal Archief Open Data Photos (CC0) — Netherlands ✅
- **What:** Dutch National Archives: ~418,000 photographs (38% of digitized photos) released as open data under CC0/public-domain marks — WWII, colonial-era Indonesia/Suriname, Dutch streets and harbors — with an API and Wikimedia Commons pipeline, high-res downloads via per-image download button.
- **URL:** https://www.nationaalarchief.nl/onderzoeken/open-data/fotos (rights: "Ruim 400.000 foto's zijn beschikbaar onder een CC0 publiek domein verklaring… U mag de foto zonder toestemming kopiëren, veranderen, en verspreiden, zelfs voor commerciële doeleinden")
- **License:** CC0 1.0 / Public Domain mark (verified on nationaalarchief.nl, 2026-10-07)
- **Free tier:** free high-res download, no account; API (XML + JPEG) for automated pulls; only CC0/PD-marked items carry a download button
- **Repo lane:** trippedd (backgrounds)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** International-equivalent entry: national (not municipal), but the cleanest CC0 government photo API found this wave. Only pull items with the download button + CC0/PD mark — items without them are still under copyright. Strong European street/harbor plates. [Wave 14 Lane B]

#### Oregon DOT Flickr — state transportation photo library ✅
- **What:** Oregon Department of Transportation's official Flickr: 17,921 photos since 2008 — highway construction, bridges, mountain passes, wildfire/smoke columns, snow operations, Columbia River Gorge — consistently licensed CC BY 2.0 per photo.
- **URL:** https://flic.kr/photos/oregondot/page150/ (rights: per-photo CC BY 2.0 — confirmed via Wikimedia Commons transfer of ODOT's "Digging Out" photo, licensed CC BY with "Author: Oregon Department of Transportation")
- **License:** CC BY 2.0 (verified via Commons file page + Flickr licensing, 2026-10-07)
- **Free tier:** free download, no account (Flickr sizes)
- **Repo lane:** trippedd (backgrounds)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Rare case of a US state DOT releasing under a clean commercial-safe license — the anti-WSDOT. Attribution required ("Oregon Department of Transportation"). Highway/bridge/mountain-pass plates and weather-event reference. [Wave 14 Lane B]

#### TNRIS / Texas Geographic Information Office DataHub — state imagery ✅
- **What:** Texas' official geospatial clearinghouse (Texas Water Development Board): statewide StratMap orthoimagery (0.5m/1m) plus a Historical Imagery Archive of 1M+ aerial frames back to the 1920s, browsable and downloadable via the DataHub.
- **URL:** https://tnris.org/education/teachers.html (DataHub launch links; rights: Texas Orthoimagery SOW v9 — "All orthoimage products will be put in the public domain and be accessible from the Texas Natural Resources Information System"; OSM Wiki: "They have informed us that all the data on the site is public domain")
- **License:** Public Domain (verified via TNRIS SOW PDF + OSM confirmation, 2026-10-07)
- **Free tier:** free download via DataHub, no account; bulk ortho tiles
- **Repo lane:** trippedd (backgrounds)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Texas city-layout and era-aerial plates at state scale. Note: already-scanned historic frames are PD, but the RDC charges $10–20/frame for new scan orders — pull only already-digitized DataHub holdings for free. [Wave 14 Lane B]

---

## 🚫 Quarantine — rights-restricted (rows 130–140 in docs/LICENSE_QUARANTINE.md)

#### NYC Municipal Archives Online Gallery — NYC Dept. of Records 🚫
- **What:** 870,000+ digitized items: 1940s/1980s tax photos (every building in the five boroughs), WPA-era collections, maps, motion pictures, audio — the deepest NYC street-plate source anywhere.
- **URL:** https://www.nyc.gov/site/records/historical-records/terms-and-conditions.page (rights: "The Municipal Archives owns the rights to its photographs and accepts applications for permission to use them… License fees will apply to commercial uses; non-profit entities are exempt from licensing fees"; portal.311.nyc.gov: "You can request permission to publish, reprint, broadcast, or duplicate photographs")
- **License:** All rights reserved by the City; commercial use requires license + fees (verified 2026-10-07)
- **Free tier:** free browsing; prints from $45; commercial licensing on application
- **Repo lane:** trippedd (backgrounds)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** QUARANTINE (row 130): the flagship municipal-rights trap — a city archive that asserts copyright and charges commercial license fees. Non-commercial/research use is exempt, so it stays usable as visual reference, but no plates in shipping assets without a license. [Wave 14 Lane B]

#### NYC Parks Photo Archive — NYC Dept. of Parks & Recreation 🚫
- **What:** 200,000+ original negatives by Parks photographers, 1856–present: parks, playgrounds, beaches, pools, plus the Moses-era construction archive (highways, bridges, housing, both World's Fairs) — much of it now in the Municipal Archives Gallery.
- **URL:** https://www.nycgovparks.org/about/history/ (rights: same DORIS/Municipal Archives regime — commercial use requires permission + license fees; DORIS blog notes the Moses-era aerials were shot by contracted commercial photographers)
- **License:** All rights reserved; commercial license fees (verified via DORIS terms, 2026-10-07)
- **Free tier:** free browsing of web exhibits
- **Repo lane:** trippedd (backgrounds)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** QUARANTINE (row 131): double trap — (1) same commercial-fee regime as the Municipal Archives, and (2) the famous aerials were shot by *contracted commercial photographers*, i.e., third-party copyright inside a city collection. Reference only. [Wave 14 Lane B]

#### WSDOT Flickr — Washington State DOT 🚫
- **What:** Washington State DOT's official Flickr: thousands of highway, bridge, ferry, mountain-pass, and construction photos (16M+ views; media reuse worldwide) — but under a Creative Commons license with NC+ND restrictions.
- **URL:** https://wsdot.wa.gov/about/current-employees/web-toolkit/photo-and-video-standards (rights: "WSDOT applies a Creative Commons license to the images we post on Flickr. This license allows anyone to copy and share our images with some restrictions"; Wikipedia file record for a WSDOT image confirms CC-BY-NC-ND 2.0)
- **License:** CC BY-NC-ND 2.0 (verified 2026-10-07)
- **Free tier:** free viewing/download, no account
- **Repo lane:** trippedd (backgrounds)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** QUARANTINE (row 132): the state-DOT trap in its purest form — Washington State asserts copyright on its works (states are not covered by federal §105), and chose NC-ND. Non-commercial reference only; no derivatives, no commercial plates. Contrast with Oregon DOT (CC BY, ✅ this wave). [Wave 14 Lane B]

#### Missouri Valley Special Collections — Kansas City Public Library 🚫
- **What:** KCPL's local-history digital collections (kchistory.org + pendergastkc.org): Kansas City street scenes, the 1951 flood, Pendergast-era politics, Monarchs baseball, 1923 zoning maps — deep Midwestern urban plates.
- **URL:** https://kchistory.org/audio/interview-elida-cardenas (rights: "Reproduction (printing, downloading, or copying) of images from Kansas City Public Library requires permission and payment for the following uses, whether digital or print: publication; reproduction of multiple copies; personal, non-educational purposes; and advertising or commercial purposes")
- **License:** Permission + use fees required for publication/commercial use (verified 2026-10-07)
- **Free tier:** free browsing; private study/scholarship/research only without permission
- **Repo lane:** trippedd (backgrounds)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** QUARANTINE (row 133): a public library that monetizes image reuse — commercial plates require paid permission. Reference browsing only. [Wave 14 Lane B]

#### James K. Hosmer Special Collections — Hennepin County Library 🚫
- **What:** Minneapolis/Hennepin County history via the Minnesota Digital Library: 19th–early-20th-century photographs, plat books, maps, trade cards, hotel menus — hundreds of period street/business plates.
- **URL:** https://mndigital.org/about/contributing-organizations/hennepin-county-library (rights: HathiTrust record for a Hosmer item — "This image may not be reproduced for any reason without the express written consent of the Hennepin County Library")
- **License:** All rights reserved; written consent required for any reproduction (verified 2026-10-07)
- **Free tier:** free browsing via Minnesota Digital Library / DPLA
- **Repo lane:** trippedd (backgrounds)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** QUARANTINE (row 134): one of the most restrictive stances found — reproduction requires express written consent "for any reason." Reference only. [Wave 14 Lane B]

#### Austin History Center — Austin Public Library 🚫
- **What:** Austin/Travis County pictorial collections: 8,000+ assets on Portal to Texas History plus a digital collections platform — streets, music venues, floods, growth-era aerials.
- **URL:** http://library.austintexas.gov/ahc/reproduction-policies-and-procedures (rights: "Images are not to be altered, published, or publicly displayed without permission of the AHC Photo Curator… permission will be granted to the customer for one-time use only"; use fees apply for publication/display; $38 digital download for previously digitized items)
- **License:** Publication/display requires permission + use fees; one-time use only (verified 2026-10-07)
- **Free tier:** free browsing; low-res web downloads; fees for files and any publication use
- **Repo lane:** trippedd (backgrounds)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** QUARANTINE (row 135): no-alteration + one-time-use + fee terms make this unusable for production plates. Reference only. [Wave 14 Lane B]

#### Center for Sacramento History — city/county joint-powers archive 🚫
- **What:** Official repository for Sacramento city/county government records plus the Sacramento Bee photo lab and McClatchy/Stanford collections — largest local-history repository on the West Coast, 1849–2000s.
- **URL:** https://www.centerforsacramentohistory.org/collections-research/using-our-collections (rights: "CSH retains all rights to the collections requested for reproduction. Permission for publication is granted for one-time, nonexclusive use"; photo use fees $10–$200/image; $25/10-image scan fee)
- **License:** All rights retained; permission + per-image use fees (verified 2026-10-07)
- **Free tier:** free on-site research; online catalog browsing
- **Repo lane:** trippedd (backgrounds)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** QUARANTINE (row 136): joint-powers government agency that still asserts full rights and charges per-image. Reference only. [Wave 14 Lane B]

#### Arizona Memory Project — AZ State Library, Archives and Public Records 🚫
- **What:** Arizona State Archives historic photographs (Capitol, Phoenix streets, desert towns, Route 66 corridor) served through the Arizona Memory Project portal.
- **URL:** https://azmemory.azlibrary.gov/nodes/view/238119 (rights: "Copyright and/or publication rights for all photographs in this collection are retained by this institution. For assistance with permission to re-use or other reference questions, please contact the Archives")
- **License:** All rights retained by the State Archives; permission required for re-use (verified 2026-10-07)
- **Free tier:** free browsing
- **Repo lane:** trippedd (backgrounds)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** QUARANTINE (row 137): state archives explicitly retaining copyright — the opposite of Florida Memory's free-use statute. Reference only. [Wave 14 Lane B]

#### Maryland State Archives — photographic collections 🚫
- **What:** Maryland State Archives + Baltimore City Archives (hosted at msa.maryland.gov): state and Baltimore municipal photographic series, with some scans on the Baltimore City Archives Flickr.
- **URL:** https://msa.maryland.gov/msa/refserv/html/use.html (rights: "Permission is required for any and all materials, including both Government/Public Records and Special Collections… Commercial uses include… websites, books, videos"; fee schedule: $75/image commercial up to 100k copies, $150 over)
- **License:** Permission required for all uses; commercial fees $75–150/image (verified 2026-10-07)
- **Free tier:** free browsing
- **Repo lane:** trippedd (backgrounds)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** QUARANTINE (row 138): permission required "for any and all materials" — even government/public records. Reference only. [Wave 14 Lane B]

#### Chicago Public Library Special Collections — digital collections 🚫
- **What:** CPL Special Collections digital holdings (neighborhoods, transit, industry, lakefront) — a municipal-library archive with genuinely unclear reuse terms.
- **URL:** https://chipublib.demo.bibliocms.com/wp-content/uploads/sites/3/2017/11/photo-reproduction-form-11-2017.pdf (rights: "Items reproduced for commercial purposes and/or publication may be subject to copyright restrictions… Users assume all responsibility for questions of copyright, invasion of privacy and rights of publicity")
- **License:** Unclear — commercial/publication use "may be subject to copyright restrictions," no PD statement (verified 2026-10-07)
- **Free tier:** free browsing; reproductions for personal/scholarly use
- **Repo lane:** trippedd (backgrounds)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** QUARANTINE (row 139): unclear rights + user-assumes-all-risk terms. Reference only until a per-collection rights statement exists. [Wave 14 Lane B]

#### King County GIS Open Data — county imagery portal 🚫
- **What:** King County (WA) GIS open-data site + iMap: aerial orthophoto basemaps (1936–2017 vintages, 3-inch urban resolution), parcel/building layers — strong Seattle-area plate/reference source.
- **URL:** https://kingcounty.gov/es-es/dept/kcit/data-information-services/gis-center/about/terms-conditions-copyrights (rights: "King County grants you a limited, revocable license to use, reproduce, and redistribute the Data… no one is permitted to sell this information except in accordance with a written agreement"; iMap aerials credited to Pictometry/EagleView contractors)
- **License:** Custom county license — use/reproduce/redistribute allowed, resale prohibited without agreement; aerials are contractor-owned (verified 2026-10-07)
- **Free tier:** free download via GIS open-data site, no account; legend "Data provided by permission of King County" required
- **Repo lane:** trippedd (backgrounds)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** QUARANTINE (row 140): the no-resale clause plus contractor-owned aerials (Pictometry/EagleView) make commercial plate use legally murky — embedding county aerials in a commercial game risks tripping both the resale clause and the contractor's copyright. Reference/layout use only without legal review. [Wave 14 Lane B]

---

## ❓ Mixed / unverified — per-item checks required

#### PhillyHistory.org — Philadelphia Dept. of Records ❓
- **What:** Philadelphia City Archives' online face: ~2M municipal photos (late 1800s+), 34,000+ digitized and searchable — City Hall construction, Mummers, transit, sanitation, JFK at Independence Hall.
- **URL:** https://opendataphilly.org/datasets/phillyhistoryorg/ (rights: "The City of Philadelphia reserves all rights in the database and any data contained therein, and the end user's use of the data does not constitute a transfer of, nor does the end user receive, any title or interest in the database or any other City data")
- **License:** ❓ Unverified — city reserves all rights; no photo-level PD statement found (checked 2026-10-07)
- **Free tier:** free browsing; prints purchasable
- **Repo lane:** trippedd (backgrounds)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Pre-1929 photos are PD by age regardless, but the city's all-rights-reserved posture means post-1928 material needs per-item clearance. Treat as a finder, not a plate source, until rights are pinned. [Wave 14 Lane B]

#### Portland City Archives (Efiles) — City of Portland, OR ❓
- **What:** Portland's official archives online database (Efiles): city records since 1851, with scanned photographs including the 1883 Davidson panorama of Central/East Portland and 1958–1974 aerials of downtown.
- **URL:** https://www.portland.gov/archives/archives (rights: no reuse/rights statement found on the archives pages — records are described as publicly accessible, but no copyright/PD terms published)
- **License:** ❓ Unverified — no rights statement located (checked 2026-10-07)
- **Free tier:** free browsing of Efiles, no records request needed
- **Repo lane:** trippedd (backgrounds)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Strong Pacific-Northwest street-plate potential (regrade-era, Vanport, harbor) but genuinely unpinable — the city publishes no reuse terms. Contact the archives for a rights statement before any production pull. [Wave 14 Lane B]

#### City of Vancouver Archives — searcharchives.vancouver.ca ❓
- **What:** Vancouver's municipal archives database: 6,900 newly digitized 1978/1986 heritage-survey photos plus the full civic collection — streets, harbor, Gastown, West End.
- **URL:** https://searcharchives.vancouver.ca/torchbearer-photographs-day-36 (rights: per-item "Terms governing use, reproduction, and publication" + "Rights" fields — e.g., 2010 torch-relay photos list "Copyright: VANOC")
- **License:** ❓ Mixed per item — some civic photos PD by age, others carry third-party copyright (checked 2026-10-07)
- **Free tier:** free browsing, no account
- **Repo lane:** trippedd (backgrounds)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Per-item rights fields exist (good), but statuses vary by fonds — only pull items explicitly marked PD/public-domain. The 1978/1986 heritage-survey set is the most promising plate batch. [Wave 14 Lane B]

#### Amsterdam Beeldbank (Image Bank) — Stadsarchief Amsterdam ❓
- **What:** Amsterdam City Archives' image bank: 260,000+ photos, prints, and building drawings, searchable by street name/keyword/date with high-res downloads — canals, Jordaan streets, harbor, WWII.
- **URL:** https://www.amsterdam.nl/stadsarchief/praktische/beeldbank/ (rights: high-res downloads offered, but no reuse/license terms found on the Beeldbank pages)
- **License:** ❓ Unverified — no clear reuse terms located (checked 2026-10-07)
- **Free tier:** free high-res download, no account
- **Repo lane:** trippedd (backgrounds)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Excellent European canal-street plates, but the archive publishes no license — unlike the Dutch Nationaal Archief (CC0, ✅ this wave). Per-item age check + archive contact needed before production use. [Wave 14 Lane B]

#### Baltimore City Archives (Flickr) — City of Baltimore ❓
- **What:** Baltimore City Archives' official Flickr stream (hosted/linked via the Maryland State Archives site): scanned municipal photo series — streets, harbor, rowhouses, public works.
- **URL:** https://msa.maryland.gov/bca/photographs-at-the-baltimore-city-archives/index.html (rights: "Some have been scanned and put up online on our Flickr page" — no reuse/rights statement on the page)
- **License:** ❓ Unverified — no rights statement located (checked 2026-10-07)
- **Free tier:** free browsing via Flickr
- **Repo lane:** trippedd (backgrounds)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Municipal archive with online photos but zero published reuse terms; note the Maryland State Archives (its host, 🚫 row 138) charges commercial fees — do not assume the Flickr stream is freer than the host's policy. [Wave 14 Lane B]

#### Tacoma Public Library Northwest Room Image Archive — City of Tacoma ❓
- **What:** Tacoma Public Library's (city department) Northwest Room: 1M+ photographic images held, 35,000+ digitized in a CONTENTdm Image Archive — waterfront, lumber mills, downtown, Mt. Rainier views.
- **URL:** https://cdm17061.contentdm.oclc.org/digital/collection/p17061coll21 (rights: no reuse/rights statement found on the Image Archive or Northwest Room pages)
- **License:** ❓ Unverified — no rights statement located (checked 2026-10-07)
- **Free tier:** free browsing/download via CONTENTdm, no account
- **Repo lane:** trippedd (backgrounds)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Strong PNW industrial/waterfront plates, but no published reuse terms — TPL is a city department, not a PD guarantee. Per-item age check + archive contact before production use. [Wave 14 Lane B]

#### Tennessee Virtual Archive (TeVA) — TN State Library & Archives ❓
- **What:** TeVA: open-access digital repository of the Tennessee State Library & Archives — thousands of photographs, postcards, maps, film, audio on Tennessee history and culture; many items downloadable free with a courtesy line.
- **URL:** https://sos.tn.gov/tsla/services/imaging-services-fee-schedule (rights: "Materials at the Library & Archives are available for purposes of education, personal use, historical research, and other 'fair use' as defined by U.S. Copyright Law… The Library & Archives does not assign rights or license materials. Users are solely responsible for determining the copyright status of items")
- **License:** ❓ Unverified — archive grants no rights and assigns no license; per-item determination required (checked 2026-10-07)
- **Free tier:** free browsing; many items free to download with "Courtesy of the Tennessee State Library & Archives" line
- **Repo lane:** trippedd (backgrounds)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** The archive explicitly refuses to clear rights — fair-use-only posture. Usable as reference; production plates need per-item copyright research. (Owner note: TN is the owner's home state — Memphis/Nashville street plates would be valuable if rights get pinned.) [Wave 14 Lane B]

---

*Lane B complete: 7 ✅ verified entries, 11 🚫 quarantine entries (rows 130–140), 7 ❓ mixed/unverified entries. All rights statuses checked against upstream sources on 2026-10-07. Skipped as failing the lane bar: Denver Public Library (Wave 13 — commercial fees), SFPL Historical Photographs (Wave 13 — permission + fees), LAPL Tessa (Wave 13 — mixed/Shades of L.A. non-commercial), Houston Public Library HMRC (no verifiable rights statement), New Orleans Public Library Louisiana Division (no verifiable rights statement), Oregon State Archives (no verifiable online photo-rights statement), Utah State Historical Society (no verifiable rights statement), Library of Virginia (no verifiable digital-collections rights statement), NY State Archives (no verifiable rights statement; NYS Parks charges use fees).*
