ZTF Avro Schemas
================

These documents are for schema v1.8.

## Schema Heirarchy

ZTF uses nested schemas to organize the data in the alert packet.

`ztf.alert` (defined in [`alert.avsc`](https://github.com/ZwickyTransientFacility/ztf-avro-alert/blob/master/schema/alert.avsc)) is the top-level namespace.  `ztf.alert` in turn relies on [`candidate.avsc`](https://github.com/ZwickyTransientFacility/ztf-avro-alert/blob/master/schema/candidate.avsc), [`prv_candidate.avsc`](https://github.com/ZwickyTransientFacility/ztf-avro-alert/blob/master/schema/prv_candidate.avsc), and [`cutout.avsc`](https://github.com/ZwickyTransientFacility/ztf-avro-alert/blob/master/schema/cutout.avsc).


### ztf.alert

The top-level alert contains the following fields:

| Field | Type | Contents |
|:--------|:-------|:--------|
| `objectId` | long | unique identifier for this object |
| `candid` | long | unique identifier for the subtraction candidate |
| `candidate` | `ztf.alert.candidate` | candidate record |
| `prv_candidates` | array of `ztf.alert.prv_candidate` or null | candidate records for 30 days' past history |
| `cutoutScience` | `ztf.alert.cutout` or null  | cutout of the science image |
| `cutoutTemplate` | `ztf.alert.cutout` or null  | cutout of the coadded reference image |
| `cutoutDifference` | `ztf.alert.cutout` or null  | cutout of the resulting difference image |


### ztf.alert.candidate

| Field | Type | Contents |
|:--------|:-------|:--------|
| `jd` | double | Observation Julian date at start of exposure [days] | 
| `fid` | int | Filter ID (1=g; 2=r; 3=i) | 
| `pid` | long | Processing ID for image | 
| `diffmaglim` | [float, null], default: null | 5-sigma mag limit in difference image based on PSF-fit photometry [mag] | 
| `pdiffimfilename` | [string, null], default: null | filename of positive (sci minus ref) difference image | 
| `programpi` | [string, null], default: null | Principal investigator attached to program ID | 
| `programid` | int | Program ID: encodes either public, collab, or caltech mode | 
| `candid` | long | Candidate ID from operations DB | 
| `isdiffpos` | string | t or 1 => candidate is from positive (sci minus ref) subtraction; f or 0 => candidate is from negative (ref minus sci) subtraction | 
| `tblid` | [long, null], default: null | Internal pipeline table extraction ID | 
| `nid` | [int, null], default: null | Night ID | 
| `rcid` | [int, null], default: null | Readout channel ID [00 .. 63] | 
| `field` | [int, null], default: null | ZTF field ID | 
| `xpos` | [float, null], default: null | x-image position of candidate [pixels] | 
| `ypos` | [float, null], default: null | y-image position of candidate [pixels] | 
| `ra` | double | Right Ascension of candidate; J2000 [deg] | 
| `dec` | double | Declination of candidate; J2000 [deg] | 
| `magpsf` | float | magnitude from PSF-fit photometry [mag] | 
| `sigmapsf` | float | 1-sigma uncertainty in magpsf [mag] | 
| `chipsf` | [float, null], default: null | Reduced chi-square for PSF-fit | 
| `magap` | [float, null], default: null | Aperture mag using 8 pixel diameter aperture [mag] | 
| `sigmagap` | [float, null], default: null | 1-sigma uncertainty in magap [mag] | 
| `distnr` | [float, null], default: null | distance to nearest source in reference image PSF-catalog [pixels] | 
| `magnr` | [float, null], default: null | magnitude of nearest source in reference image PSF-catalog [mag] | 
| `sigmagnr` | [float, null], default: null | 1-sigma uncertainty in magnr [mag] | 
| `chinr` | [float, null], default: null | DAOPhot chi parameter of nearest source in reference image PSF-catalog | 
| `sharpnr` | [float, null], default: null | DAOPhot sharp parameter of nearest source in reference image PSF-catalog | 
| `sky` | [float, null], default: null | Local sky background estimate [DN] | 
| `magdiff` | [float, null], default: null | Difference: magap - magpsf [mag] | 
| `fwhm` | [float, null], default: null | Full Width Half Max assuming a Gaussian core, from SExtractor [pixels] | 
| `classtar` | [float, null], default: null | Star/Galaxy classification score from SExtractor | 
| `mindtoedge` | [float, null], default: null | Distance to nearest edge in image [pixels] | 
| `magfromlim` | [float, null], default: null | Difference: diffmaglim - magap [mag] | 
| `seeratio` | [float, null], default: null | Ratio: difffwhm / fwhm | 
| `aimage` | [float, null], default: null | Windowed profile RMS afloat major axis from SExtractor [pixels] | 
| `bimage` | [float, null], default: null | Windowed profile RMS afloat minor axis from SExtractor [pixels] | 
| `aimagerat` | [float, null], default: null | Ratio: aimage / fwhm | 
| `bimagerat` | [float, null], default: null | Ratio: bimage / fwhm | 
| `elong` | [float, null], default: null | Ratio: aimage / bimage | 
| `nneg` | [int, null], default: null | number of negative pixels in a 5 x 5 pixel stamp | 
| `nbad` | [int, null], default: null | number of prior-tagged bad pixels in a 5 x 5 pixel stamp | 
| `rb` | [float, null], default: null | RealBogus quality score; range is 0 to 1 where closer to 1 is more reliable | 
| `ssdistnr` | [float, null], default: null | distance to nearest known solar system object [arcsec] | 
| `ssmagnr` | [float, null], default: null | magnitude of nearest known solar system object (usually V-band from MPC archive) [mag] | 
| `ssnamenr` | [string, null], default: null | name of nearest known solar system object (from MPC archive) | 
| `sumrat` | [float, null], default: null | Ratio: sum(pixels) / sum(abs(pixels)) in a 5 x 5 pixel stamp where stamp is first median-filtered to mitigate outliers | 
| `magapbig` | [float, null], default: null | Aperture mag using 18 pixel diameter aperture [mag] | 
| `sigmagapbig` | [float, null], default: null | 1-sigma uncertainty in magapbig [mag] | 
| `ranr` | double | Right Ascension of nearest source in reference image PSF-catalog; J2000 [deg] | 
| `decnr` | double | Declination of nearest source in reference image PSF-catalog; J2000 [deg] | 
| `ndethist` | int | Number of spatially-coincident detections falling within 1.5 arcsec going back to beginning of survey; only detections that fell on the same field and readout-channel ID where the input candidate was observed are counted | 
| `ncovhist` | int | Number of times input candidate position fell on any field and readout-channel going back to beginning of survey | 
| `jdstarthist` | [double, null], default: null | Earliest Julian date of epoch corresponding to ndethist [days] | 
| `jdendhist` | [double, null], default: null | Latest Julian date of epoch corresponding to ndethist [days] |
| `scorr` |  [double, null],   default: null |  Peak-pixel signal-to-noise ratio in point source matched-filtered detection image | 
| `tooflag` |  [int, null],  default: 0 |  1 => candidate is from a Target-of-Opportunity (ToO) exposure; 0 => candidate is from a non-ToO exposure | 
| `objectidps1` |  [long,  null],  default: null |  Object ID of closest source from PS1 catalog; if exists within 30 arcsec | 
| `sgmag1` | [float, null], default: null | g-band PSF magnitude of closest source from PS1 catalog; if exists within 30 arcsec [mag] | 
| `srmag1` | [float, null], default: null | r-band PSF magnitude of closest source from PS1 catalog; if exists within 30 arcsec [mag] | 
| `simag1` | [float, null], default: null | i-band PSF magnitude of closest source from PS1 catalog; if exists within 30 arcsec [mag] | 
| `szmag1` | [float, null], default: null | z-band PSF magnitude of closest source from PS1 catalog; if exists within 30 arcsec [mag] | 
| `sgscore1` | [float, null], default: null | Star/Galaxy score of closest source from PS1 catalog 0 <= sgscore <= 1 where closer to 1 implies higher likelihood of being a star | 
| `distpsnr1` | [float, null], default: null | Distance of closest source from PS1 catalog; if exists within 30 arcsec [arcsec] |
| `objectidps2` |  [long,  null],  default: null |  Object ID of second closest source from PS1 catalog; if exists within 30 arcsec | 
| `sgmag2` |  [float,  null],  default: null |  g-band PSF magnitude of second closest source from PS1 catalog; if exists within 30 arcsec [mag] | 
| `srmag2` |  [float,  null],  default: null |  r-band PSF magnitude of second closest source from PS1 catalog; if exists within 30 arcsec [mag] | 
| `simag2` |  [float,  null],  default: null |  i-band PSF magnitude of second closest source from PS1 catalog; if exists within 30 arcsec [mag] | 
| `szmag2` |  [float,  null],  default: null |  z-band PSF magnitude of second closest source from PS1 catalog; if exists within 30 arcsec [mag] | 
| `sgscore2` |  [float,  null],  default: null |  Star/Galaxy score of second closest source from PS1 catalog; if exists within 30 arcsec: 0 <= sgscore <= 1 where closer to 1 implies higher likelihood of being a star | 
| `distpsnr2` |  [float,  null],  default: null |  Distance to second closest source from PS1 catalog; if exists within 30 arcsec [arcsec] | 
| `objectidps3` |  [long, null],  default: null |  Object ID of third closest source from PS1 catalog; if exists within 30 arcsec | 
| `sgmag3` |  [float, null],  default: null |  g-band PSF magnitude of third closest source from PS1 catalog; if exists within 30 arcsec [mag] | 
| `srmag3` |  [float, null],  default: null |  r-band PSF magnitude of third closest source from PS1 catalog; if exists within 30 arcsec [mag] | 
| `simag3` |  [float, null],  default: null |  i-band PSF magnitude of third closest source from PS1 catalog; if exists within 30 arcsec [mag] | 
| `szmag3` |  [float, null],  default: null |  z-band PSF magnitude of third closest source from PS1 catalog; if exists within 30 arcsec [mag] | 
| `sgscore3` |  [float,  null],  default: null |  Star/Galaxy score of third closest source from PS1 catalog; if exists within 30 arcsec: 0 <= sgscore <= 1 where closer to 1 implies higher likelihood of being a star | 
| `distpsnr3` |  [float,  null],  default: null |  Distance to third closest source from PS1 catalog; if exists within 30 arcsec [arcsec] | 
| `nmtchps` |  int |  Number of source matches from PS1 catalog falling within 30 arcsec | 
| `rfid` |  long |  Processing ID for reference image to facilitate archive retrieval | 
| `jdstartref` |  double |  Observation Julian date of earliest exposure used to generate reference image [days] | 
| `jdendref` |  double |  Observation Julian date of latest exposure used to generate reference image [days] | 
| `nframesref` |  int |  Number of frames (epochal images) used to generate reference image |



### ztf.alert.prv_candidate

The `prv_candidates` field contains an array of one or more previous subtraction candidates at the position of the alert.  These are obtained by a simple cone search at the position of the alert candidate on the last 30 days of history.  If there are no previous candidates or upper limits, this field is null.

The fields for an individual `prv_candidate` are identical to `candidate` except for the omission of the PS1 matches (`sgmag#`, `srmag#`, `simag#`, `szmag#`, `sgscore#`, `distpsnr#`, `objectidps#`, `nmatchps`), previous detection history (`ndethist`, `ncovhist`, `jdstarthist`, `jdendhist`), `tooflag`,  and reference image information (`rfid`, `jdstartref`, `jdendref`, `nframesref`).

Additionally, if the previous image has a nondetection at position of the new candidate, `candid`, `isdiffpos`, `ra`, `dec`, `magpsf`, `sigmapsf`, `ranr`, and `decr` will be null.  In this case `diffmaglim` provides an estimate of the limiting magnitude over the entire image.

### ztf.alert.cutout

Each cutout contains two fields:

| Field | Type | Contents |
|:--------|:-------|:-------|
| `fileName` | string | Original cutout location |
| `stampData` | bytes | gzip-compressed FITS cutout image |
