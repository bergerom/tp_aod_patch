#include "patch.hpp"

Patch::Patch(void) {
    this->previous_patch = NULL ;
    this->patch_atom = NULL ;
    this->cost = 0 ;
}

Patch::Patch(const std::shared_ptr<Patch> &previous_patch, const std::shared_ptr<PatchAtom> &patch_atom) {
    this->previous_patch = previous_patch ;
    this->patch_atom = patch_atom ;
    this->cost = this->previous_patch->cost + this->patch_atom->compute_cost() ;
}

int Patch::getCost(void) const {
    return this->cost ;
}

std::list<std::shared_ptr<PatchAtom>> Patch::getAtoms(void) const {
    std::list<std::shared_ptr<PatchAtom>> atom_list ;
    std::shared_ptr<Patch> ptr = std::make_shared<Patch>(*this) ;
    while(ptr->previous_patch != NULL) {
        atom_list.push_front(ptr->patch_atom) ;
        ptr = ptr->previous_patch ;
    }
    return atom_list ;
}

void Patch::printInStream(std::ostream &stream) const {
    auto atom_list = this->getAtoms() ;
    for(auto atom : atom_list) {
        atom->printInStream(stream) ;
    }
}
