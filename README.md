# image-harbor

Image organization and management software. This is an evolving document and will change frequently as updates are made.

## Application Goals (Mission / 10,000ft View)

- Add photos once ive digitized them
- Added images are copied to the application's working image store directory (probably AppData/Image Harbor)
- Be able to identify which roll of photos a picture came from
- Be able to identify when a photo was taken and with what camera lense and film
- Be able to preview images and flag ones i want to edit
- Segregate images that need to be edited
- Export a folder of the images that need to be edited
- Once they are edited, be able to tie back the edited version with its original (and original to its edited version)
- Do basic image edits within the software (mainly rotate) which modify the Harbor image (no the original but our copied one)
- Export as different file formats to desired location (this exported file isnt tracked anywhere in the app its just if i need the image somewhere else)
- Do metadata edits like changing the image name, lens used, film stock, camera used
- Make arbitrary image collections (including images in disperate batches)
- Export image collections/rolls etc as zip to desired location
- Rate images to help identify which are the best (0-5 stars?)
  - Idea: could display images rated at that star level as a hover over preview to help you figure out if the image is good enough for a 3 or 5 star rating
- Continuously back up images to a local drive AND/OR to a cloud image solution
- Continuously back up datastore containing metadata and relationships to a local drive AND/OR to a cloud storage solution
- Be able to restore from a back up in the event of catastrophic data loss
- Should be focused on local and individual use for orgonizing my work

## How can this be achieved? WIP

Fundamentally we have images and collections (groupings of images), this seems like the most simple abstraction around the needs of the app. This should be able to manage not necessarily only analog photography, but also digital photos where rolls dont make any sense

A roll of film has many images. when adding a new roll of film's worth of images, they could be added to a Collection, a Collection that represents that roll of film.

Seems that there are some attributes images can have, but there are also attributes collections can have. Some of these are binary, but some are more like key/value pairs.

Images or collections could have tags, tags could just be things that describe the image or collection of images. They **could** be key value parios but it might not be necessary?

Imagine a collection of images from a single roll of film. That film may have tags like pentax, 35mm, mx, ilford hp5, bw, downtown, knoxville, street, etc... effectivly the #hashtag model.
Some properties should be their own proper fields like name, date_produced, description

some properties are really dependant on the type of image, like digital artwork doesnt have a camera or film stock. so what if there was some abstraction over the metadata fields, like an archetype.

the archetype could define key/value pairs that every asset of that archetype must have? that seems clunky and inflexable. unnessessarily complicated.

if it were just collections and images i dont see how this wouldnt cover all the needs of the 10000 foot view? what if collections had a type field, most collections would end up with a type of "user_defined" but for analog film for example it could have a type of "film_roll", or even having collections that just say all these xyz images were added at the same time like in the case of digital images where there is no definite roll that groups images. something like "import_group".

then collections can have name, description, tags, _type,_created_ts,_last_updated_ts for example

With that in mind, image assets could also have similar name, description, tags, produced_date, rating, file_path, derrived_from,_created_ts,_last_updated_ts
Expanding on this rating doesnt need to be its own field. rating can itself be a collection, or is that taking things too far? having reserved collections for _1_star, _2_star, ..., _5_star... i guess this is more like an idea of a generated or dynamic collection? like a collection that isnt static but is built on the fly like using a query. Still something to think about but rating should probably be tied to the image asset

---

UPDATED

Reasonable ideas but flawed because there is differences in the many-to-many and one-to-many relatiuonships going on here.
For example, an image will onyl every belong to one import group and one film_roll but many user defined collections.
I should stay focused on a MVP, thinking abvout digital art is not relevant, focus on cameras and photography analog and digital.

with that in mind, i should have concrete fields for a lot of this info and just leave them null when they arnty applicable.
Also i should make clear that the image isnt being stored in this app, instead the image exists on disk and is referenced inside the app. With the idea that when you impor images i will copy it to a, "Image Harbor" folder probably in the "Pictures" directory on your system. so the binaries of the images wont be stored in the database.

## Tech Stack

- python
- sqlite

## Abstract Data Model

### image_assets

- id
- name
- description
- format*
- camera_make*
- camera_model*
- lens*
- captured_year*
- captured_month*
- captured_day*
- rating
  - from 0 to 5 stars
- needs_editing
- file_id
- edited_from_id
  - this is when images are edited in external applications like lightroom and re-imported as "edited" images
  - does not apply to edit-in-place operations like rotation
- belongs_to_roll_id
- imported_in_group_id
- _created_ts
- _last_updated_ts

NOTE: fields ending in * will override roll value if roll id present, if not present, if not will join to the roll transparently or be handled in service layer

### files

- id
- path
  - path to local image within harbor image store
- thumbnail_path
  - path to thumbnail image within harbor preview store
  - e.g. 150x150
- preview_path
  - path to preview image within harbor preview store
  - e.g. 720x720
- mime_type
- width
- height
- orientation
  - portrait, landscape, square
- size
- hash
- original_filename
- original_size
- original_last_modified_ts
- original_path
  - path to the original image that was copied when this was imported

### film_rolls

- id
- name
- description
- camera_make
- camera_model
- format
- stock
- lens
- captured_year
- captured_month
- captured_day
- created_ts
- last_updated_ts

### user_collections

- id
- name
- description
- created_ts
- last_updated_ts

### user_collections_to_image_assets

- user_collection_id
- image_asset_id

### import_groups

- id
- import_ts

### tags

- id
- name

### tag_to_image_asset

- tag_id
- image_asset_id
