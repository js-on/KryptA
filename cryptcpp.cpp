#include <stdio.h>
#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include <cmath>
#include <iomanip>
#include <algorithm>

#define BIT_LENGTH 8

int PROG_WIDTH = 50;
bool DEBUG = true;
std::vector<std::string> boilerplate = {};

/**
 * @brief Check whether vector has only unique items or not
 * 
 * @tparam T type of vector items
 * @param x vector
 * @return true if vector is unique
 * @return false if duplicate eitems exist
 */
template <class T>
bool is_unique(std::vector<T> &x) {
    std::sort( x.begin(), x.end() ); // O(N log N)
    return std::adjacent_find( x.begin(), x.end() ) == x.end();
}

/**
 * @brief Convert binary string to integer
 * 
 * @param bin binary string
 * @return int 
 */
int binToInt(std::string bin) {
    return std::stoi(bin, 0, 2);
}

/**
 * @brief Convert integer to binary string with fixed size
 * 
 * @param num integer to convert
 * @param length fixed size; ignored if
 * @return std::string 
 */
std::string intToBin(int num, int length) {
    std::string res = "";
    while (num > 0) {
        res = std::to_string(num % 2) + res;
        num = (int)num/2;
    }
    while (res.size() < length) {
        res = "0" + res;
    }
    return res;
}

/**
 * @brief Convert string vector to int vector
 * 
 * @param vector 
 * @return std::vector<int> 
 */
std::vector<int> strVectorToInt(std::vector<std::string> vector) {
    std::vector<int> res;
    for (auto &it : vector) {
        res.push_back(std::stoi(it, 0, 2));
    }
    return res;
}

/**
 * @brief Count character in string
 * 
 * @param string String to search in
 * @param chr Character to search for
 * @return unsigned int 
 */
int countStr(std::string string, char chr) {
    size_t pos = 0;
    int count = 0;
    while ((pos = string.find(chr, pos)) < string.length()) {
        count++;
        pos++;
    }
    return count;
}

/**
 * @brief Print progress bar
 * 
 * @param pos current index in main loop
 * @param size number of planned iterations
 * @return int 
 */
int progress(int pos, int size)
{
    std::string msg = "Progress: [";
    int length = int((pos * PROG_WIDTH) / size + 1);
    for (int i = 0; i < length; i++)
    {
        msg.append("#");
    }
    for (int i = 0; i < PROG_WIDTH - length; i++)
    {
        msg.append(" ");
    }
    msg.append("]");
    std::cout << msg << "\r";
    return 0;
}

/**
 * @brief Struct to hold ratings of an sbox
 * 
 */
struct rating
{
    int quality;
    int quantity;
    std::vector<std::string> sbox;
};

/**
 * @brief Print usage information and exit(0)
 * 
 * @return int 
 */
int help()
{
    std::cout << "Give one of the following parameters:" << std::endl;
    std::cout << "\t-test\n\tTest s-boxes stored asbox.csv in sbox.csv" << std::endl;
    std::cout << "\t-loop <iterations> [<number of boxes>]\n\tGenerate X s-boxes to find best possible" << std::endl;
    exit(EXIT_SUCCESS);
}

/**
 * @brief Split string at separator
 * 
 * @param string string to split
 * @param separator delimiter
 * @return std::vector<std::string> 
 */
std::vector<std::string> splitString(std::string string, char separator) {
    int pos = 0;
    std::vector<std::string> res;
    while ((pos = string.find(separator)) != std::string::npos) {
        res.push_back(string.substr(0, pos));
        string = string.substr(pos+1, string.size());
    }
    res.push_back(string);
    return res;
}

/**
 * @brief Join vector of strings in CSV style
 * 
 * @param vector string vector to join
 * @return std::string
 */
std::string joinVector(std::vector<std::string> vector, std::string separator)
{
    std::string res;
    for (auto &it : vector)
    {
        res.append(it);
        res.append(separator);
    }
    res.pop_back();
    return res;
}

/**
 * @brief Check if vector elements are unique and length is power of two
 * 
 * @param sbox vector of binary numbers as strings
 * @return bool
 */
bool validateSbox(std::vector<std::string> sbox)
{
    if (is_unique(sbox) && (sbox.size() & (sbox.size() - 1)) % 2 == 0) {
        return true;
    }
    return false;
}

/**
 * @brief Read s-boxes from CSV file 
 * 
 * @param filename File storing the s-boxes
 * @return std::vector<std::string> 
 */
std::vector<std::vector<std::string>> readSbox(std::string filename)
{
    std::string line;
    std::ifstream csv;
    std::vector<std::vector<std::string>> data;
    csv.open("sbox.csv");

    if (!csv.is_open())
    {
        std::cout << "File sbox.csv is already in use.\nPlease close the file and try again.\n";
        exit(EXIT_FAILURE);
    }
    while (std::getline(csv, line))
    {
        // FIXME: Remove debug output
        // std::cout << line << "\n";
        std::vector<std::string> temp = splitString(line, ',');
        // for (auto &it : temp) {
        //     std::cout << it << " ";
        // }
        // std::cout << "\n";
        if (validateSbox(temp)) {
            data.push_back(temp);
        }
        else {
            std::cout << "Something went wrong parsing your sbox.\nPlease ensure that its elements are unique and its size is a power of 2.\n";
            exit(EXIT_FAILURE);
        }
    }
    return data;
}

/**
 * @brief Calculate linear approximation for input bit to output bit via given S-Box
 * 
 * @param sbox sbox to analyze
 * @param input_bit input bit
 * @param output_bit expected output bit
 * @return unsigned int 
 */
unsigned int linearApprox(std::vector<int> sbox, int input_bit, int output_bit) {
    unsigned int total = 0;
    // FIXME: Remove debug output
    // std::cout << input_bit << " . " << output_bit << ". ";
    // for (auto &it : sbox) {
    //     std::cout << it << " ";
    // }
    // std::cout << "\n";
    for (int ii = 0; ii < sbox.size(); ii++) {
        int input_masked = ii & output_bit;
        int output_masked = sbox[ii] & output_bit;
        // TODO: Dynamic BIT_LENGTH
        std::string input_masked_bin = intToBin(input_masked, BIT_LENGTH);
        std::string output_masked_bin = intToBin(output_masked, BIT_LENGTH);
        if ((countStr(input_masked_bin, '1') - countStr(output_masked_bin, '1')) % 2 == 0) {
            total++;
        }
    }
    return total;
}

/**
 * @brief Method to analyze s-box
 * 
 * @param sbox vector of binary numbers as strings
 * @param debug print proximity table or not
 * @return rating 
 */
rating rateSbox(std::vector<std::string> sbox, bool debug)
{
    // debug = false;
    std::vector<int> box = strVectorToInt(sbox);
    unsigned int quality = 0;
    unsigned int quantity = 0;
    unsigned int mean = int(box.size())/2;
    if (debug) {
        std::cout << "  / ";
        for (int i = 0; i < box.size(); i++) {
            std::cout << std::right << std::setw(3) << std::to_string(i) << " ";
        }
        std::cout << "\n";
        std::string line = " ";
        for (int i = 0; i < box.size()+1; i++) {
            line.append("----");
        }
        std::cout << line << "\n";
    }
    for (int row = 0; row < box.size(); row++) {
        if (debug) {
            std::cout << std::right << std::setw(3) << std::to_string(row) << " ";
        }
        for (int col = 0; col < box.size(); col++) {
            unsigned int res = linearApprox(box, row, col);
            if (debug) {
                std::cout << std::right << std::setw(3) << std::to_string(res) << " ";
            }
            if (res != mean) {
                quality = quality + pow(mean - res, 2);
                quantity++;
            }
        }
        if (debug) {
            std::cout << "\n";
        }
    }
    if (debug) {
        std::cout << "Quantity: " << quantity << "\n";
        std::cout << "Quality:  " << quality << "\n";

    }
    rating res;
    res.quality = quality;
    res.quantity = quantity;
    res.sbox = sbox;
    return res;
}

/**
 * @brief Get a random sbox
 * 
 * @return std::vector<std::string> 
 */
std::vector<std::string> getRandomSbox()
{
    std::vector<std::string> sbox = {};
    return sbox;
}

/**
 * @brief Main driver
 * 
 * @param argc number of arguments
 * @param argv char array containing arguments
 * @return int 
 */
int main(int argc, char const *argv[])
{
    /* Arguments missing */
    if (argc == 1)
    {
        help();
    }
    /* Test sboxes in sbox.csv */
    else if ((std::string)argv[1] == "-test")
    {
        std::vector<std::vector<std::string>> boxes = readSbox("sbox.csv");
        rateSbox(boxes[0], true);
    }
    /* Loop n times to generate x sboxes */
    else if ((std::string)argv[1] == "-loop")
    {
        int rng;
        int box_count;
        int box_length;
        /* parse arguments */
        if (argc == 5)
        {
            /* number of iterations */
            rng = std::atoi(argv[2]);
            if (rng < 1)
            {
                std::cout << "Range must be a valid and positive number\n";
                exit(EXIT_FAILURE);
            }
            /* number of boxes to generate */
            int box_count = std::atoi(argv[3]);
            if (box_count < 1)
            {
                std::cout << "Box count must be a valid and positive number\n";
                exit(EXIT_FAILURE);
            }
            /* length of boxes to generate */
            int box_length = std::atoi(argv[4]);
            /* check size and if power of 2 */
            if (box_length < 4 && (box_length & (box_length - 1)) == 0)
            {
                std::cout << "Box length must be a valid number and a power of 2.\n";
            }
        }
        /* too many arguments */
        else
        {
            std::cout << "You need to pass a range like `-loop <iterations> <number of boxes> <size of boxes>`\n";
            exit(EXIT_FAILURE);
        }

        /* Craft object with all ratings and boxes */
        std::vector<rating> ratings;
        for (int i = 0; i < box_count; i++)
        {
            rating temp = {0, 0, {}};
            ratings.push_back(temp);
        }

        /* start iterating to search for "optimized" sbox */
        for (int i = 0; i < rng; i++)
        {
            progress(i, rng);
            /* calculate rng x box_count sboxes */
            std::vector<std::string> sbox = getRandomSbox();
            rating temp = rateSbox(sbox, false);
            for (int i = 0; i < ratings.size(); i++)
            {
                if (temp.quality > ratings[i].quality || temp.quantity > ratings[i].quantity)
                {
                    ratings[i] = temp;
                    break;
                }
            }

            /* print results */
            for (int i = 0; i < ratings.size(); i++)
            {
                std::cout << "S" << i + 1 << "\n";
                std::cout << "Quality:  " << ratings[i].quality << "\n";
                std::cout << "Quantity: " << ratings[i].quantity << "\n";
                std::cout << "S-Box:    " << joinVector(ratings[i].sbox, ",") << "\n\n";
            }
        }
    }
    /* Unknown parameter */
    else
    {
        help();
    }
    std::cout << std::endl;

    return 0;
}