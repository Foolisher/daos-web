#!/usr/bin/env bash

base_idr=`pwd`

cd ${base_idr}/static/scripts && rm all.js
cat jquery.min.js >> all.js
echo "" >> all.js

for jsfile in `ls`; do
	[ ${jsfile} != 'all.js' ] && [ ${jsfile} != 'jquery.min.js' ] && \
	echo -e "\n\n/* $jsfile */" >> all.js && cat ${jsfile} >> all.js
done

echo `du -h all.js`

cd ${base_idr}/static/styles && rm all.css

for cssfile in `ls`; do
	[ ${cssfile} != 'all.css' ] && [ ${cssfile} != 'prism.css' ] && \
	echo -e "\n\n/* $cssfile */" >> all.css && cat ${cssfile} >> all.css
done
 
echo `du -h all.css`

