#import "SearchView.h"
#import "WikiApp.h"

#define MAXRES 10

int nresults = 0;
uint32_t blocks[MAXRES];
char *matches[MAXRES];
char *buf;

bool chandleResult(char *s) {
  NSLog(@"chandleResult: %s", s);
  buf = xalloc(MAXSTR * sizeof(char));
  strcpy(buf, s);

  NSLog(@"buf: 0x%x, %s", buf, buf);

  char *blockpos = strrchr(buf, ' ');
  int c;

  if(nresults >= MAXRES) return false;

  if(blockpos) {
    *(blockpos - 1) = '\0'; 
    blockpos++;

    blocks[nresults] = atoi(blockpos);

    matches[nresults] = buf;
  } else
    fatal("invalid: '%s'", buf);

  NSLog(@"chandleResult returning...");
  return ++nresults < MAXRES;
}

void zeroResults() { 
  int i;
  for(i = 0; i < nresults; i++) free(matches[i]);
  nresults = 0;
}
int numResults() { return nresults; }
char *resultAt(int i) { return matches[i]; }
uint32_t blockAt(int i) { return blocks[i]; }

@implementation SearchView

-(void) initMatches {
  int i;
  for(i = 0; i < MAXRES; i++)
    matches[i] = xalloc(MAXSTR * sizeof(char));
  buf = NULL;
}

-(id) initWithFrame: (struct CGRect) frame
{
  self = [super initWithFrame: frame];  

  curNeedle = xalloc(MAXSTR * sizeof(char));
  [self initMatches];
  sthread = nil;
  lock = [[NSRecursiveLock alloc] init];

  struct CGRect rect = [UIHardware fullScreenApplicationContentRect];
  //TODO: re-enable me when I want progress bar
  //table = [[UICompletionTable alloc] initWithFrame: CGRectMake(0, 0, frame.size.width, frame.size.height - 240)];
  table = [[UICompletionTable alloc] initWithFrame: CGRectMake(0, 0, frame.size.width, frame.size.height - 215)];

  [table setDelegate: self];

  [self addSubview: table];

  prog = [[UIProgressBar alloc] initWithFrame: CGRectMake(0, 180, 320, 20)];
  [prog setStyle: 0];
  [prog setProgress: 1.0];
  //[self addSubview: prog];
  //TODO: re-enable above to get progress bar

  kbrd = [[UIKeyboard alloc] initWithFrame: CGRectMake(0, 200, 320, 480)];
	[self addSubview: kbrd];

  dump = xalloc(sizeof(wp_dump));

  load_dump(dump,
      "/var/root/wp/processed",
      "/var/root/wp/locate.db",
      "/var/root/wp/locate.prefixdb",
      "/var/root/wp/blocks.db");

  updater = [NSTimer scheduledTimerWithTimeInterval: 1 
           target: self
           selector: @selector(refreshResults:)
           userInfo: nil
           repeats: YES]; 

  return self; 
}

-(void) stopSearch {
  NSLog(@"stopSearch");
  kill_search();
  while(sthread && [sthread isExecuting]) {
    //usleep(100000);
    //NSLog(@"waiting for sthread");
  }
}


-(void) runSearch {
  NSLog(@"runSearch with needle: '%s'", curNeedle);
  NSAutoreleasePool* pool = [NSAutoreleasePool new];
  search(&dump->index, curNeedle, &chandleResult, NULL, true, true); 
  needRefresh = true;
  NSLog(@"search done");
  [pool release];
}

-(void) refreshResults: (NSTimer *) timer {
  NSLog(@"refreshResults");
  [lock lock];
  if(needRefresh || (sthread && [sthread isExecuting])) {
    [table reloadData];
    if(needRefresh) needRefresh = false;
  }
  double d;
  search_progress(&dump->index, &d);
  [prog setProgress: d];
  [prog updateIfNecessary];
  [lock unlock];
}

-(void) updateResults {
  NSLog(@"Updating results for '%@'", needle);
  [self stopSearch];
  zeroResults();
  curResults = 0;
  needRefresh = false;

  /* TODO: keep the table results that match the new needle */
  [table reloadData];
  [prog setProgress: 0.0];

  strncpy(curNeedle, [[needle capitalizedString] UTF8String], MAXSTR);

  sthread = [[NSThread alloc] initWithTarget: self selector: @selector(runSearch) object: nil];
  [sthread start];
}

-(int) numberOfCompletionsInTable:(UICompletionTable *) t {
  return numResults();
}

-(UITableCell *) table:(UITable *)t completionAtIndex: (int) index {
  return [NSString stringWithUTF8String: resultAt(index)];
}

-(void) table: (UICompletionTable *) t didSelectCompletionAtIndex: (int) i {
  [aview loadArticle: [NSString stringWithUTF8String: resultAt(i)] fromBlock: blockAt(i)];
  [parent switchToArticle];
}

- (void) setParent: (WikiApp *) w {
  parent = w;
}

-(void) setNeedle: (NSString *) s {
  [lock lock];
  needle = s;

  if([s length] > 0 && [s characterAtIndex: 0] != ' ')
    [self updateResults];
  [lock unlock];
}

- (void) setArticleView: (ArticleView *) a {
  aview = a;
  [aview setDump: dump];
}
@end
