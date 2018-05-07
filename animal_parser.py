import sys
import requests
from bs4 import BeautifulSoup

class AnimalParser:

    def run(self, args):
        if ('--help' in args) | ('-h' in args):
            self.show_help()
            sys.exit()
        self.parse()
        print('Succesfully parsed animals!')
        if '--correct' in args:
            self.correct()
        print('Bye!')
        sys.exit()

    def parse(self):
        self.parse_to_dict()
        self.write_list_to_file(self.animal_dict.keys(), 'parsed_animals')


    def correct(self):
        print('Correcting parsed animals... ', end='')
        corrected_animal_list = self.correct_animal_names()
        print('Done')
        self.write_list_to_file(corrected_animal_list, 'corrected_animals')


    def show_help(self):
        print('use --correct if you want to correct the names of the animals')


    def parse_to_dict(self):
        page = requests.get('http://www.studio-evenaar.nl/parken/register.php')
        soup = BeautifulSoup(page.content, 'html.parser')
        animal_list = soup.select('td.kop3 a')
        self.animal_dict = {item.get_text(): 'http://www.studio-evenaar.nl' + item['href'][2:] for item in animal_list}


    def write_list_to_file(self, list_, filename):
        print('Writing list to file {}... '.format(filename), end='')
        with open(filename, 'w') as file:
            for item in list_:
                file.write('%s\n' % item)
        print('Done')


    def correct_animal_names(self):
        print('Correcting animal names... ')
        corrected_animal_list = []
        for animal_url in self.animal_dict.values():
            #print(animal_url)
            animal_page = requests.get(animal_url)
            animal_soup = BeautifulSoup(animal_page.content, 'html.parser')
            animal_page_title = animal_soup.title.string
            animal_corrected_name = animal_page_title.split('-')[0]
            corrected_animal_list.append(animal_corrected_name)
            print('Corrected: ' + animal_corrected_name + " " * 25, end='\r')
        print('Done!')
        return sorted(set(corrected_animal_list))


if __name__ == "__main__":
    parser = AnimalParser()
    parser.run(sys.argv)

