#!/bin/bash

if [[ $TERM =~ 256 ]]; then
	echo ~/.mutt/themes/calmar.light
else
	echo ~/.mutt/themes/themes.default
fi
