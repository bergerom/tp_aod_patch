#include "patch.hpp"

class TabPatch {
private:
    std::vector<std::string> file_in ;
    std::vector<std::string> file_out ;
    std::vector<std::shared_ptr<Patch>> previous_patch ;
    std::vector<std::shared_ptr<Patch>> current_patch ;
    void init(const std::vector<std::string> &file_in, const std::vector<std::string> &file_out) ;

public:
    TabPatch(const std::string &file_in, const std::string &file_out) ;
    TabPatch(const std::vector<std::string> &file_in, const std::vector<std::string> &file_out) ;

};
