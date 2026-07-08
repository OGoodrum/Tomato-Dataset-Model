const imageArea = document.querySelector('.imageArea');

import {
  S3Client,
  ListBucketsCommand,
  ListObjectsV2Command,
  GetObjectCommand,
  PutObjectCommand,
} from "@aws-sdk/client-s3";

const S3 = new S3Client({
  region: "auto", // Required by SDK but not used by R2
  // Provide your Cloudflare account ID
  endpoint: `https://${ACCOUNT_ID}.r2.cloudflarestorage.com`,
  // Retrieve your S3 API credentials for your R2 bucket via API tokens (see: https://developers.cloudflare.com/r2/api/tokens)
  credentials: {
    accessKeyId: ACCESS_KEY_ID,
    secretAccessKey: SECRET_ACCESS_KEY,
  },
});

let images = [];

function updateImageArea() {
    let newInnerHTML = '';
    images.forEach((image, index) => {
        newInnerHTML += `
        <li class="image-container"><img src=${image} width="640" height="480" /></li>
        `
    });

    imageArea.innerHTML = newInnerHTML;
}

updateImageArea();