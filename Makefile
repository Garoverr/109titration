##
## EPITECH PROJECT, 2023
## 104intersection
## File description:
## makefile
##

NAME	=	109titration

SRC	=	109titration.py

$(NAME):
	cp $(SRC) $(NAME)
	chmod 755 $(NAME)

all:	$(NAME)
