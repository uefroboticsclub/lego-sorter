## Overview
This project is a LEGO sorting system using a Jetson Nano, a single top-down camera, and a conveyor belt. The system:
1. Captures an image of a LEGO piece.
2. Sends it to the [Brickognize API](https://api.brickognize.com/) for identification.
3. Determines which bin the piece belongs to (4 predefined categories or an "unidentified" bin).
4. Uses a servo-controlled paddle to sort the piece into the correct bin.

---

## Using the Brickognize API
To predict a LEGO piece using the API, run this command in the terminal:

```bash
curl -X 'POST' 'https://api.brickognize.com/predict/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'query_image=@your-image-file.jpg;type=image/jpeg' | python -m json.tool
```

### Explanation:
- `query_image=@your-image-file.jpg` → Specifies the **image file** to send.
- `| python -m json.tool` → Formats the API response for readability.
- **Ensure the image file exists** in the correct directory!
  - If it's in `Pictures/Webcam/`, specify:
    ```bash
    -F 'query_image=@Pictures/Webcam/my-image.jpg;type=image/jpeg'
    ```
  - Or navigate to that folder first:
    ```bash
    cd ~/Pictures/Webcam
    curl -X 'POST' 'https://api.brickognize.com/predict/' \
      -H 'accept: application/json' \
      -H 'Content-Type: multipart/form-data' \
      -F 'query_image=@my-image.jpg;type=image/jpeg' | python -m json.tool
    ```
