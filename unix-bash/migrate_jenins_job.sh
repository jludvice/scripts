#!/bin/env bash


OLD_JENKINS="jenkins url"
NEW_JENKINS="jenkins url"


JOB_NAME="existing job namee"
NEW_NAME="name of job to be created or updated with existing job name"

echo "your login?: "
read user

echo "your password"
read -s password


# store config.xml
curl -u "${user}:${password}" -s "${OLD_JENKINS}/job/${JOB_NAME}/config.xml" > "${JOB_NAME}.xml"
echo "job stored to ${JOB_NAME}.xml"


# check if job exists
response=$(curl --write-out %{http_code} --silent --output /dev/null ${NEW_JENKINS}/job/${NEW_NAME})

if [ $response -eq "404" ]; then
  echo "creating new job ${NEW_NAME}"
  curl -u "${user}:${password}" -X POST "${NEW_JENKINS}/createItem?name=${NEW_NAME}" --header "Content-Type: application/xml" --data-binary @${JOB_NAME}.xml

else
  echo "updating existing job ${NEW_NAME}"
  curl -u "${user}:${password}" -X POST -s "${NEW_JENKINS}/job/${NEW_NAME}/config.xml" --header "Content-Type: application/xml" --data-binary @${JOB_NAME}.xml

fi


echo ""
echo "Done, check your new job at ${NEW_JENKINS}/job/${NEW_NAME}"
echo ""
