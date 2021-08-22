#!/bin/bash

images=$(cat local.yml | grep 'smartats.azurecr.io/smart_ats' | cut -d ":" -f 2)
for image in $images
do
  docker tag $image $image:${GITHUB_SHA:-latest}
done
