#include <memory>
#include <vector>
#include <fstream>
#include "computePatch.hpp"

void TabPatch::init(const std::vector<std::string> &file_in, const std::vector<std::string> &file_out) {
    this->file_in = file_in ;
    this->file_out = file_out ;
    this->previous_patch = std::vector<std::shared_ptr<Patch>>(file_in.size(), NULL) ;
    this->current_patch = std::vector<std::shared_ptr<Patch>>(file_in.size(), NULL) ;
}

// Commence l'indiçage à 1.
std::vector<std::string> readlines(std::string file_name) {
    std::string line ;
    std::ifstream file(file_name) ;
    std::vector<std::string> line_vector ;
    line_vector.push_back("") ;
    while(std::getline(file, line)) {
        line_vector.push_back(line) ;
    }
    return line_vector ;
}

TabPatch::TabPatch(const std::string &file_in, const std::string &file_out) {
    this->init(readlines(file_in), readlines(file_out)) ;
}

// On suppose que l'indiçage commence à 1.
TabPatch::TabPatch(const std::vector<std::string> &file_in, const std::vector<std::string> &file_out) {
    this->init(file_in, file_out) ;
}
