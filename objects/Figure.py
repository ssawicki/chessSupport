from abc import ABC, abstractmethod

import numpy as np

from exceptions import MoveNotPermittedError
from settings import CHESS_BOARD, CHESS_DIAGONALS, CHESS_CARDINALS
from utils import get_field_coordinates, is_in_bounds


class Figure(ABC):
    def __init__(self, field: str):
        self.field = field

    @abstractmethod
    def list_available_moves(self):
        pass

    @abstractmethod
    def validate_move(self, dest_field):
        pass


class Context:
    def __init__(self, strategy: Figure) -> None:
        self._strategy = strategy

    def list_moves(self) -> list:
        result = self._strategy.list_available_moves()
        return result

    def validate_move(self, dest_field: str) -> None:
        self._strategy.validate_move(dest_field)


class King(Figure):
    def list_available_moves(self) -> list:
        x, y = get_field_coordinates(self.field)
        available_moves = list()
        for xx, yy in self.__king_list(x, y):
            if is_in_bounds(xx, yy):
                available_moves.append((xx, yy))
        Y = np.transpose(available_moves)[0]
        X = np.transpose(available_moves)[1]
        available_moves = CHESS_BOARD[Y, X]
        return available_moves.tolist()

    def validate_move(self, dest_field: str) -> None:
        available_moves = self.list_available_moves()
        if dest_field not in available_moves:
            raise MoveNotPermittedError("Current move is not permitted.")

    def __king_list(self, x: int, y: int) -> list:
        return [
            (x + 1, y),
            (x + 1, y + 1),
            (x + 1, y - 1),
            (x, y + 1),
            (x, y - 1),
            (x - 1, y),
            (x - 1, y + 1),
            (x - 1, y - 1),
        ]


class Pawn(Figure):
    def list_available_moves(self) -> list:
        available_moves, error = list(), None
        x, y = get_field_coordinates(self.field)
        field_name, field_number = self.__get_field_pole()
        new_field_number = field_number + 1
        available_moves.append(f"{field_name}{new_field_number}")
        return available_moves

    def validate_move(self, dest_field: str) -> None:
        valid_move = self.list_available_moves()
        if dest_field not in valid_move:
            raise MoveNotPermittedError("Current move is not permitted.")

    def __get_field_pole(self) -> [str, int]:
        field_number = int(self.field[1])
        field_name = self.field[0]
        return field_name, field_number


class Queen(Figure):
    def list_available_moves(self) -> list:
        available_moves = list()

        x, y = get_field_coordinates(self.field)
        for xint, yint in CHESS_DIAGONALS + CHESS_CARDINALS:
            xtemp, ytemp = x + xint, y + yint
            while is_in_bounds(xtemp, ytemp):

                available_moves.append((xtemp, ytemp))

                xtemp, ytemp = xtemp + xint, ytemp + yint

        Y = np.transpose(available_moves)[0]
        X = np.transpose(available_moves)[1]

        available_moves = CHESS_BOARD[Y, X]
        return available_moves.tolist()

    def validate_move(self, dest_field: str) -> None:
        available_moves = self.list_available_moves()
        if dest_field not in available_moves:
            raise MoveNotPermittedError("Current move is not permitted.")


class Rook(Figure):
    def list_available_moves(self) -> list:
        available_moves = list()

        x, y = get_field_coordinates(self.field)
        for xint, yint in CHESS_CARDINALS:
            xtemp, ytemp = x + xint, y + yint
            while is_in_bounds(xtemp, ytemp):

                available_moves.append((xtemp, ytemp))

                xtemp, ytemp = xtemp + xint, ytemp + yint

        Y = np.transpose(available_moves)[0]
        X = np.transpose(available_moves)[1]

        available_moves = CHESS_BOARD[Y, X]
        return available_moves.tolist()

    def validate_move(self, dest_field) -> None:
        available_moves = self.list_available_moves()
        if dest_field not in available_moves:
            raise MoveNotPermittedError("Current move is not permitted.")


class Bishop(Figure):
    def list_available_moves(self) -> list:
        available_moves = list()
        x, y = get_field_coordinates(self.field)
        for xint, yint in CHESS_DIAGONALS:
            xtemp, ytemp = x + xint, y + yint
            while is_in_bounds(xtemp, ytemp):

                available_moves.append((xtemp, ytemp))

                xtemp, ytemp = xtemp + xint, ytemp + yint

        Y = np.transpose(available_moves)[0]
        X = np.transpose(available_moves)[1]

        available_moves = CHESS_BOARD[Y, X]
        return available_moves.tolist()

    def validate_move(self, dest_field) -> None:
        available_moves = self.list_available_moves()
        if dest_field not in available_moves:
            raise MoveNotPermittedError("Current move is not permitted.")


class Knight(Figure):
    def list_available_moves(self) -> list:
        x, y = get_field_coordinates(self.field)
        available_moves = list()
        for xx, yy in self.__knight_list(x, y, 2, 1):
            if is_in_bounds(xx, yy):
                available_moves.append((xx, yy))
        Y = np.transpose(available_moves)[0]
        X = np.transpose(available_moves)[1]
        available_moves = CHESS_BOARD[Y, X]
        return available_moves.tolist()

    def validate_move(self, dest_field: str) -> None:
        available_moves = self.list_available_moves()
        if dest_field not in available_moves:
            raise MoveNotPermittedError("Current move is not permitted.")

    def __knight_list(self, x: int, y: int, int1: int, int2: int) -> list:

        return [
            (x + int1, y + int2),
            (x - int1, y + int2),
            (x + int1, y - int2),
            (x - int1, y - int2),
            (x + int2, y + int1),
            (x - int2, y + int1),
            (x + int2, y - int1),
            (x - int2, y - int1),
        ]
