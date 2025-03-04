# lego-sorter

TO PREDICT! DO THIS!!!! IN THE TERMIN!!!AL!!!!

curl -X 'POST'   'https://api.brickognize.com/predict/'   -H 'accept: application/json'   -H 'Content-Type: multipart/form-data'   -F 'query_image=@2025-03-04-171805.jpg;type=image/jpeg' | python -m json.tool

the "| python -m json.tool" formats the output so you can read it!!!

"query_image=@2025-03-04-171805.jpg" sets what image to send over the api!!!!
change the name of  the file to get it to work with whatever fi le you want!!

the file is relative to the current directory, so if you want to use a file in the Pictures/Webcam/ folder, you have to mention the directory! or cd there!!!!
