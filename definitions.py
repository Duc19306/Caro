import copy

# Khai báo hằng số X và O để đại diện cho người chơi
X = "X"
O = "O"

# TẠO BẢNG
# Hàm tạo bảng 3x3 với các ô ban đầu có giá trị là None
def create_board():
    return [[None for _ in range(3)] for _ in range(3)]
# Tạo bản sao của bảng và thực hiện hành động của người chơi
def result(board, action):
    # Tạo một bản sao sâu của bảng hiện tại
    copy_board = copy.deepcopy(board)
    # Trích xuất tọa độ i, j từ hành động
    i, j = action
    # Đặt người chơi tương ứng vào ô được chọn
    copy_board[i][j] = players(copy_board)
    # Trả về bảng mới sau khi thực hiện hành động
    return copy_board

# Xác định người chơi hiện tại dựa trên trạng thái của bảng
def players(board):
    # Đếm số lượng ô X và ô O trên bảng
    x_count = sum(row.count(X) - row.count(O) for row in board)
    # Nếu số lượng ô X và ô O bằng nhau, người chơi tiếp theo là X, ngược lại là O
    return X if x_count == 0 else O

# Kiểm tra xem bảng đã đầy chưa
def full_tiles(board):
    # Kiểm tra xem tất cả các ô trên bảng có giá trị khác None không
    return all(None not in row for row in board)

# Kiểm tra trạng thái kết thúc của trò chơi
def terminal(board):
    # Lấy tất cả các dòng trên bảng
    lines = get_all_lines(board)
    '''
    Kiểm tra xem có dòng nào có 3 ô X hoặc 3 ô O không
    Hoặc nếu bảng đã đầy và không có người chiến thắng (utility(board) == 0)
    '''
    return any(line.count(X) == 3 or line.count(O) == 3 for line in lines) or (full_tiles(board) and utility(board) == 0)

# Xác định điểm của trạng thái kết thúc của trò chơi
def utility(board):
    # Lấy tất cả các dòng trên bảng
    lines = get_all_lines(board)
    '''
    Nếu có dòng nào có 3 ô X, trạng thái này là trạng thái X thắng (điểm = 1)
    Nếu có dòng nào có 3 ô O, trạng thái này là trạng thái O thắng (điểm = -1)
    Ngược lại, trạng thái này là trạng thái hòa (điểm = 0)
    '''
    if any(line.count(X) == 3 for line in lines):
        return 1
    elif any(line.count(O) == 3 for line in lines):
        return -1
    return 0

# Lấy tất cả các dòng trên bảng
def get_all_lines(board):
    lines = []
    # Thêm tất cả các dòng của bảng vào danh sách lines
    for row in board:
        lines.append(row)
    # Thêm tất cả các cột của bảng vào danh sách lines
    for j in range(3):
        lines.append([board[i][j] for i in range(3)])
    # Thêm hai đường chéo chính của bảng vào danh sách lines
    lines.append([board[i][i] for i in range(3)])
    lines.append([board[i][2-i] for i in range(3)])
    # Trả về danh sách lines chứa tất cả các dòng trên bảng
    return lines

# Xác định người chiến thắng (nếu có) của trò chơi
def winners(board):
    # Nếu trạng thái kết thúc của trò chơi và điểm của trạng thái đó là 1,
    # người chiến thắng là X
    if terminal(board):
        if utility(board) == 1:
            return X
        # Nếu điểm của trạng thái là -1, người chiến thắng là O
        elif utility(board) == -1:
            return O
    # Nếu không có người chiến thắng, trả về None
    return None
