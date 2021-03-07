#!/bin/bash

BOARD=("-" "-" "-" "-" "-" "-" "-" "-" "-")
PLAYER="2"
FILLED_FIELDS=0
LIMIT=8
WON="0"

function display {
	clear
	echo "Board"
	echo "${BOARD[0]} | ${BOARD[1]} | ${BOARD[2]}"
	echo "${BOARD[3]} | ${BOARD[4]} | ${BOARD[5]}"
	echo "${BOARD[6]} | ${BOARD[7]} | ${BOARD[8]}"
}

function checkMatch {
	# winning conditions for player 1
  	if [ ${BOARD[$1]} == "o" ] && [ ${BOARD[$1]} == ${BOARD[$2]} ] && [ ${BOARD[$2]} == ${BOARD[$3]} ]; then
    	WON="1"
  	fi

  	# winning conditions for player 2
  	if [ ${BOARD[$1]} == "x" ] && [ ${BOARD[$1]} == ${BOARD[$2]} ] && [ ${BOARD[$2]} == ${BOARD[$3]} ]; then
    	WON="2"
  	fi
}

function checkWin {
	# horizontal
	checkMatch 0 1 2
  	checkMatch 3 4 5
  	checkMatch 6 7 8
  	# vertical
  	checkMatch 0 3 6
  	checkMatch 1 4 7
  	checkMatch 2 5 8
  	#diagonal
  	checkMatch 0 4 8
  	checkMatch 2 4 6
}

function validateInput {
	regex="^[0-8]$"
	if ! [[ $1 =~ $regex ]];
	then
		changePlayer
	fi
	# if field empty then set value
	if [ ${BOARD[$1]} == "-" ];
	then
		((FILLED_FIELDS = $FILLED_FIELDS + 1))
		if [ $PLAYER -eq 2 ];
		then
			BOARD[$1]="x"
		else
			BOARD[$1]="o"
		fi
	else
		changePlayer
	fi
}

function changePlayer {
	if [ $PLAYER -eq 1 ];
	then
		PLAYER="2"
	else
		PLAYER="1"
	fi
}

# Check if someone won or if the whole table is filled -> no winner
while [ $WON -eq "0" ] && [ "$FILLED_FIELDS" -le "$LIMIT" ]
do
	display
	changePlayer
	echo -e "\n Select field for player ${PLAYER}"
	read FIELD

	echo ${FIELD}

	validateInput $FIELD
	checkWin
done

display
if [ $WON != "0" ];
then
	echo "The game is DONE! Winning player is Player ${WON}"
else
	echo "The game is DONE! No winner in this round"
fi
