

class MazeDrawing():
    def __init__(self, engine, maze_img):
        """Maze color, cell_size, line_thickness"""
        self.edge_size = 50
        self.edge_color: int = 0x2121DE
        self.line_thickness = 6
        self.engine = engine
        self.maze_img = maze_img

    def _get_thickness(self, middle: int) -> tuple[int, int]:
        """Calculate the offset for maze line thickness"""
        y0 = middle - (self.line_thickness // 2)
        y1 = middle + (self.line_thickness // 2)
        return (y0, y1)

    def _get_real_pos(self, index_x: int, index_y: int) -> tuple[int, int]:
        """Convert grid coordinates (column, row)
        to screen pixel coordinates."""
        pos_x = index_x * self.edge_size + self.engine.x_padding
        pos_y = index_y * self.edge_size + self.engine.y_padding
        return (pos_x, pos_y)

    def _draw_line(self, start: tuple[int, int]) -> None:
        """Draw an horizontal line from left to right"""
        x0, y_mid = start
        x1 = x0 + self.edge_size
        y0, y1 = self._get_thickness(y_mid)
        self.engine.fill_rectangle(x0, x1, y0, y1,
                                   self.edge_color, self.maze_img)

    def _draw_column(self, start: tuple[int, int]) -> None:
        """Draw a vertical line from top to bottom"""
        x_middle, y0 = start
        y1 = y0 + self.edge_size
        x0, x1 = self._get_thickness(x_middle)
        self.engine.fill_rectangle(x0, x1, y0, y1, self.edge_color,
                                   self.maze_img)

    def _draw_cell(self, cell_value: int, cell_pos: tuple[int, int]) -> None:
        """Draw walls for a single cell using bitwise masking.

        Bits convention:
            1 (0b0001): Top wall
            2 (0b0010): Right wall
            4 (0b0100): Bottom wall
            8 (0b1000): Left wall
        """
        x, y = cell_pos
        if cell_value & 1:
            self._draw_line((x, y))
        if cell_value & 2:
            self._draw_column((x + self.edge_size, y))
        if cell_value & 4:
            self._draw_line((x, y + self.edge_size))
        if cell_value & 8:
            self._draw_column((x, y))

    def draw_maze(self, maze: list[list[int]]):
        """Call the draw_cell function for each cell, effectively building
        the maze cell by cell"""
        for index_y, line in enumerate(maze):
            for index_x, cell in enumerate(line):
                cell_pos = self._get_real_pos(index_x, index_y)
                self._draw_cell(cell, cell_pos)
