#!/bin/bash
fil="$1"
sed -i.bak '/www/d' $fil
head -n -14 $fil > temp
mv temp $fil
sed -i '/^Problems/d' $fil
perl -pi -e '#Promise: \“#Promise:\n\“#g' $fil
perl -0pi -e 's/(.*\nProblem:)/About: $1/g' $fil
perl -0777 -pi -e 's/Section.*?(About)/$1/gs' $fil

perl -00 -pi -e 's/\n(?!(\"|Problem|Promise|About|Prayer))/ $1/sg' $fil #Negative Look Behind, capture group and replace new line with space
perl -pi -e "s#\. \“#\.\n\"#g"  $fil

sed -i 's/"\./"/g' $fil
sed -i 's/  / /g' $fil
sed -i 's/\- //g' $fil
sed -i 's/About: Promise:/About:/g'  $fil
sed -i 's/About: Condition:/About:/g'  $fil
sed -i 's/About/End_ Start_/g' $fil
sed -i '1d' $fil
sed -i -e "\$aEnd_" $fil

python fp.py $fil
