class ImageConversion:

    @staticmethod
    def convert_file_to_binary(filename):
        with open(filename, 'rb') as file:
            binary_data = file.read()
        return binary_data

    @staticmethod
    def convert_binary_to_file(binary_data, filename):
        with open(filename, 'wb') as file:
            file.write(binary_data)
        return filename
