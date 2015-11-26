#include <string>
#include <iostream>

class PatchAtom {
protected:
    int line_nb ;

public:
    PatchAtom(int line_nb) ;
    virtual int compute_cost(void) const = 0 ;
    virtual void printInStream(std::ostream &stream) const = 0 ;
};

class IdentityAtom : public PatchAtom {
public:
    IdentityAtom(int line_nb) ;
    int compute_cost(void) const = 0 ;
    void printInStream(std::ostream &stream) const ;
};

class AdditionAtom : public PatchAtom {
private:
    std::string new_line ;

public:
    AdditionAtom(int line_nb, const std::string &new_line) ;
    int compute_cost(void) const = 0 ;
    void printInStream(std::ostream &stream) const ;
};

class SubstituteAtom : public PatchAtom {
private:
    std::string subs_line ;

public:
    SubstituteAtom(int line_nb, const std::string &subs_line) ;
    int compute_cost(void) const = 0 ;
    void printInStream(std::ostream &stream) const ;
};

class DestructionAtom : public PatchAtom {
public:
    DestructionAtom(int line_nb) ;
    int compute_cost(void) const = 0 ;
    void printInStream(std::ostream &stream) const ;
};

class DestructionMultAtom : public PatchAtom {
private:
    int size ;

public:
    DestructionMultAtom(int line_nb, int size) ;
    int compute_cost(void) const = 0 ;
    void printInStream(std::ostream &stream) const ;
};
