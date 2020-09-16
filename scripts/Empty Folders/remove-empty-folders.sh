#!/system/bin/sh

# get directory list 
find . -type d -print > dirs$$
# reverse the listing 
tail -r dirs$$ > revdirs$$ 

while read dirname
do
    rmdir $dirname 2>/dev/null
done < revdirs$$
# clean up 
rm dirs$$
rm -rf revdirs$$
