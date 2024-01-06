import pygame
import csv

pygame.init()

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

input_num = 1
scale_x = 5
scale_y = 5
invailed_input = False

class OutputBox:
    def __init__(self, x, y, width, height, font_size=20, font_color=(255, 255, 255), bg_color="gray"):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(None, font_size)
        self.font_color = font_color
        self.bg_color = bg_color
        self.text = ""

    def set_text(self, text):
        if len(text) >= 169 and len(text) <= 330:
            text = text[:169] + "\n" + text[169:]
        elif len(text) > 330 and len(text) <= 399:
            text = text[:169] + "\n" + text[169:]
            text = text[:330] + "\n" + text[330:]
        elif len(text) > 490:
            text = text[:169] + "\n" + text[169:]
            text = text[:330] + "\n" + text[330:]
            text = text[:490] + "\n" + text[490:]
            
        self.text = text

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect)
        lines = self.text.split('\n')
        y = self.rect.y
        for line in lines:
            text_surface = self.font.render(line, True, self.font_color)
            screen.blit(text_surface, (self.rect.x + 10, y + 5))
            y += self.font.get_height() + 5

class TextBox:
    def __init__(self, x, y, width, height, font_size=50):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(None, font_size)
        self.color_inactive = pygame.Color('#78E4FF')
        self.color_active = pygame.Color('#1F7F7D')
        self.color = self.color_inactive
        self.active = False
        self.text = ''
        self.text_surface = self.font.render(self.text, True, self.color)
        self.width = max(width, self.text_surface.get_width() + 10)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                
                if event.key == pygame.K_RETURN:
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.unicode.isdigit() or event.unicode == "-" and len(self.text) == 0:
                    self.text += event.unicode
                self.width = max(self.rect.width, self.text_surface.get_width() + 10)
                self.text_surface = self.font.render(self.text, True, self.color)

    def update(self):
        global input_num
        self.rect.w = self.width
        input_num = self.text

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2)
        screen.blit(self.text_surface, (self.rect.x + 5, self.rect.y + 5))

class Button:
    def __init__(self, x, y, width, height, text, text_size, button_color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.button_color = button_color
        self.text_color = text_color
        self.font = pygame.font.Font(None, text_size)

    def draw(self, screen):
        pygame.draw.rect(screen, self.button_color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

add_button_x = Button(1170, 500, 100, 100, "+", 120, "green", "white")
remove_button_x = Button(1170, 610, 100, 100, "-", 150, "red", "white")

add_button_y = Button(1060, 500, 100, 100, "+", 120, "green", "white")
remove_button_y = Button(1060, 610, 100, 100, "-", 150, "red", "white")

save_button = Button(1120, 10, 150, 50, "Save", 50, "green", "white")

text_box = TextBox(130, 10, 140, 45)

text_input = text_box.font.render("INPUT:", True, text_box.color)

output_box = OutputBox(20, 70, 1000, 100)

x_text = text_box.font.render("X", True, 'white')
y_text = text_box.font.render("Y", True, 'white')

def algorithm(input):
    output = []
    if input == "" or input == "-":
        input = 1
        invailed_input = True
    else:
        invailed_input = False
    input = int(input)
    output.append(input)
    seen_numbers = set()
    repeating_numbers = False

    for num in output:
        if num in seen_numbers:
            repeating_numbers = True
        else:
            seen_numbers.add(num)
    while repeating_numbers == False:
        if (input % 2 == 0):
            input /= 2
        else:
            input = input * 3 + 1
        output.append(int(input))
        seen_numbers = set()
        for num in output:
            if num in seen_numbers:
                repeating_numbers = True
            else:
                seen_numbers.add(num)
    return output

def update_points(points):
    new_points = []
    for i, j in points:
        new_points.append((i,j+720))
    return new_points

def prepare_y(inp):
    global input_num
    output = []
    if input_num == "" or input_num == "-":
        input_num = 1
    if(int(input_num) < 0):
        for y in inp:
            output.append(y)
    else:
        for y in inp:
            output.append(-y)
    return output

def make_points(inp,scale_x,scale_y):
    points = []
    count = 0
    for y in inp:
        points.append((count,y*scale_y))
        count = count + (10*scale_x)
    points.append((0,720))
    points.append(points[0])
    return points

def save():
    global input_num
    if input_num == "":
        input_num = 5

    data = algorithm(input_num)
    data = data[0:len(data)-1]

    csv_filename = 'Collatz Conjecture Data.csv'

    # Open the CSV file in append mode or create a new file if it doesn't exist
    with open(csv_filename, 'a+', newline='') as csv_file:
        # Create a CSV writer object
        csv_writer = csv.writer(csv_file)

        # Check if the file is empty, and write a header if needed
        if csv_file.tell() == 0:
            header = ['#', 'Starting Seed', 'Result']
            csv_writer.writerow(header)  # Header

        # Move the file cursor to the beginning for reading existing rows
        csv_file.seek(0)

        # Get the current row number by counting existing rows
        current_row_number = sum(1 for _ in csv.reader(csv_file)) + 1

        # Move the file cursor back to the end for appending new rows
        csv_file.seek(0, 2)

        # Write the list to the CSV file with the current row number and items
        csv_writer.writerow([current_row_number-1] + data)


points = update_points(make_points(prepare_y(algorithm(input_num)),scale_x,scale_y))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if add_button_x.is_clicked(pygame.mouse.get_pos()):
                scale_x += 0.2
            if remove_button_x.is_clicked(pygame.mouse.get_pos()):
                scale_x -= 0.2
            if add_button_x.is_clicked(pygame.mouse.get_pos()):
                scale_x += 0.2
            if remove_button_x.is_clicked(pygame.mouse.get_pos()):
                scale_x -= 0.2
            if add_button_y.is_clicked(pygame.mouse.get_pos()):
                scale_y += 0.2
            if remove_button_y.is_clicked(pygame.mouse.get_pos()):
                scale_y -= 0.2


            if save_button.is_clicked(pygame.mouse.get_pos()):
                save()
        text_box.handle_event(event)

    screen.fill("black")
    
    pygame.draw.polygon(screen, "#0088FF",points)

    add_button_x.draw(screen)
    remove_button_x.draw(screen)
    add_button_y.draw(screen)
    remove_button_y.draw(screen)
    save_button.draw(screen)

    text_input = text_box.font.render("INPUT:", True, text_box.color)
    screen.blit(text_input, (10, 15))

    screen.blit(x_text, (1207, 450))
    screen.blit(y_text, (1097, 450))

    output_text = "OUTPUT:\n"+str(algorithm(input_num))
    output_box.set_text(output_text)
    output_box.draw(screen)

    text_box.update()
    text_box.draw(screen)

    points = update_points(make_points(prepare_y(algorithm(input_num)),scale_x, scale_y))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()