//
// Offline Wikipedia database interface for Python
// (or any other SWIG supported language)
//
// Module functions are prefixed with 'wp_' to avoid clashes with functions
// defined in wp.h.

// Note that the Ruby Inline implementation used a '__' prefix, but that won't
// work in Python as the underscores cause the methods to be treated as private.
//
%module wp

%{
#include "../../c/wp.h"

#define MAXRES 40
#define MAXSTR 1024

wp_dump d = {0};
wp_article a = {0};

char results[MAXRES][MAXSTR];
int nresults;

bool __handle_result(char *s) {
  strncpy(results[nresults], s, MAXSTR);
  results[nresults][MAXSTR - 1] = '\0';
  char *end = strrchr(results[nresults], ' ');

  if(end) {
    *(end - 1) = '\0';
    nresults++;
  }

  return nresults < MAXRES;
}

void wp_load_dump(char *dump, char *loc, char *ploc, char *blocks) {
  load_dump(&d, dump, loc, ploc, blocks);
  init_article(&a);
}

char *wp_load_article(char *name) {
  a.block = 0;
  a.text[0] = '\0';
  load_article(&d, name, &a);
  return a.text;
}

int wp_article_block() {
  return a.block;
}

int wp_article_size() {
  return strlen(a.text);
}

int wp_search(char *needle) {
  nresults = 0;
  search(&d.index, needle, __handle_result, NULL, true, true);
  return nresults;
}

char *wp_result(int n) {
  return results[n];
}

%}

void wp_load_dump(char *dump, char *loc, char *ploc, char *blocks);

char *wp_load_article(char *name);
int wp_article_block();
int wp_article_size();

int wp_search(char *needle);
char *wp_result(int n);
