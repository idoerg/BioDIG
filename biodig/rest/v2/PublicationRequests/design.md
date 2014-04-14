PublicationJob
---------------------
id
image_id
status
dateCreated


POST   -- Create publication request (use image_id)
LIST   -- Lists all the publication requests
GET    -- Gets the information about the request
PUT    -- Fulfills the request (runs the job)
       -- Sets image with id isPrivate = False
       -- Searches for all tag groups with dateCreated <= request.dateCreated
           -- Sets isPrivate = False for each tag group
       -- Searches for all tags belonging to those tag groups with dateCreated <= request.dateCreated
           -- Sets isPrivate = False for each tag
       -- Searches for all gene links belonging to those tags with dateCreated <= request.dateCreated
           -- Sets isPrivate = False for each gene link
DELETE -- Cancels the publication job (only works if the job is not yet running)
