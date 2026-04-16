# image-harbor
Image organization and management software. This is an evolving document and will change frequently as updates are made.


## 10000 foot view

I want to

Add photos once ive digitized them

Be able to identify which roll of photos a picture came from
Be able to identify when a photo was taken and with what camera lense and film
Be able to preview images and flag ones i want to edit

Segregate images that need to be edited
- _to_be_edited could be a protected pre-existing collection
Export a folder of the images that need to be edited
Once they are edited, be able to tie back the edited version with its original (and original to its edited version)

Do basic image edits within the software (rotate, export as different file format)
Do metadata edits like changing the image name, lens used, film stock, camera used

Make arbitrary image collections (including images in disperate batches)

Rate images to help identify which are the best (0-5 stars?)
- Idea could display images rated at that star level as a hover over preview to help you figure out if the image is good enough for a 3 or 5 star rating

Easily (and continuously) back up images to a local drive AND/OR to a cloud image solution

## How can this be achieved?
Fundamentally we have images and collections (groupings of images), this seems like the most simple abstraction around the needs of the app.

A roll of film has many images. when adding a new roll of film's worth of images, they could be added to a Collection, a Collection that represents that roll of film.

Seems that there are some attributes images can have, but there are also attributes collections can have. Some of these are binary, but some are more like key/value pairs.

Images or collections could have tags, tags could just be things that describe the image or collection of images. They **could** be key value parios but it might not be necessary?

Imagine a collection of images from a single roll of film. That film may have tags like pentax, 35mm, mx, ilford hp5, bw, downtown, knoxville, street, etc... effectivly the #hashtag model.
Some properties should be their own fields like name, date_produced, description