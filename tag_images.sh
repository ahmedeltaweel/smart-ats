#!/bin/bash

images=$(cat production.yml | grep 'smartats.azurecr.io/smart_ats' | cut -d ":" -f 2)
for image in $images
do
  docker tag $image $image:${GITHUB_SHA:-latest}
  docker push -a $image
done
