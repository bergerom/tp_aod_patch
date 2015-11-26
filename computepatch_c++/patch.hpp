#include <memory>
#include <list>
#include "patchAtom.hpp"

class Patch {
private:
    std::shared_ptr<Patch> previous_patch ;
    std::shared_ptr<PatchAtom> patch_atom ;
    int cost ;

public:
    Patch(void) ;
    Patch(const std::shared_ptr<Patch> &previous_patch, const std::shared_ptr<PatchAtom> &patch_atom) ;
    int getCost(void) const ;
    std::list<std::shared_ptr<PatchAtom>> getAtoms(void) const ;
    void printInStream(std::ostream &stream) const ;
};

inline bool operator< (const Patch& lhs, const Patch& rhs){ return lhs.getCost() < rhs.getCost() ; }
inline bool operator> (const Patch& lhs, const Patch& rhs){return  operator< (rhs,lhs);}
inline bool operator<=(const Patch& lhs, const Patch& rhs){return !operator> (lhs,rhs);}
inline bool operator>=(const Patch& lhs, const Patch& rhs){return !operator< (lhs,rhs);}
