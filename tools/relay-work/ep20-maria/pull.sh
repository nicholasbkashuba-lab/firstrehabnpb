#!/bin/bash
# pull.sh <branch> <outfile> : fetch chunked relay branch (split -b suffixes aa..) and verify sha256
B=$1; OUT=$2; R=https://raw.githubusercontent.com/nicholasbkashuba-lab/firstrehabnpb/$B
want=$(curl -sSf $R/master.sha256 | cut -d' ' -f1)
rm -f "$OUT"; n=0
for a in a b c d; do for b in a b c d e f g h i j k l m n o p q r s t u v w x y z; do
  curl -sSfL --retry 4 "$R/master.chunk_$a$b" -o "$OUT.part" 2>/dev/null || break 2
  cat "$OUT.part" >> "$OUT"; n=$((n+1))
done; done; rm -f "$OUT.part"
got=$(sha256sum "$OUT" | cut -d' ' -f1)
echo "$B: $n chunks"; [ "$want" = "$got" ] && echo SHA_OK || { echo "SHA_MISMATCH want $want got $got"; exit 1; }
