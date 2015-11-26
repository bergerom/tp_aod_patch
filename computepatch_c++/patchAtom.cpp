#include "patchAtom.hpp"

PatchAtom::PatchAtom(int line_nb) {
    this->line_nb = line_nb ;
}

IdentityAtom::IdentityAtom(int line_nb) : PatchAtom(line_nb) {

}

int IdentityAtom::compute_cost(void) const {
    return 0 ;
}

void IdentityAtom::printInStream(std::ostream &stream) const {

}

AdditionAtom::AdditionAtom(int line_nb, const std::string &new_line) : PatchAtom(line_nb) {
    this->new_line = new_line ;
}

int AdditionAtom::compute_cost(void) const {
    return 10 + new_line.size() ;
}

void AdditionAtom::printInStream(std::ostream &stream) const {
    stream << "+" << this->line_nb << "\n" << this->new_line << "\n" ;
}

SubstituteAtom::SubstituteAtom(int line_nb, const std::string &subs_line) : PatchAtom(line_nb) {
    this->subs_line = subs_line ;
}

int SubstituteAtom::compute_cost(void) const {
    return 10 + subs_line.size() ;
}

void SubstituteAtom::printInStream(std::ostream &stream) const {
    stream << "=" << this->line_nb << "\n" << this->subs_line << "\n" ;
}

DestructionAtom::DestructionAtom(int line_nb) : PatchAtom(line_nb) {

}

int DestructionAtom::compute_cost(void) const {
    return 10 ;
}

void DestructionAtom::printInStream(std::ostream &stream) const {
    stream << "d" << this->line_nb << "\n" ;
}

DestructionMultAtom::DestructionMultAtom(int line_nb, int size) : PatchAtom(line_nb) {
    this->size = size ;
}

int DestructionMultAtom::compute_cost(void) const {
    return 15 ;
}

void DestructionMultAtom::printInStream(std::ostream &stream) const {
    stream << "D" << this->line_nb << " " << this->size << "\n" ;
}
