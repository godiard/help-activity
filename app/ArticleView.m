#import "ArticleView.h"

@implementation ArticleView
- (id) initWithFrame: (struct CGRect) frame
{
  self = [super initWithFrame:frame];

  wkv = [[WebKitView alloc] initWithFrame: frame]; //CGRectMake(0, 0, frame.size.width, frame.size.height)];
  [wkv setPolicyDelegate: self];
 
  article = xalloc(sizeof(wp_article));
  init_article(article);

  [self addSubview: wkv];
  
  return self;
}

- (BOOL)respondsToSelector:(SEL)aSelector
{
  NSLog(@"AV Request for selector: %@", NSStringFromSelector(aSelector));
  return [super respondsToSelector:aSelector];
}

- (void)webView:(WebView *)sender decidePolicyForNavigationAction:(NSDictionary *)actionInformation request:(NSURLRequest *)request frame:(WebFrame *)frame decisionListener:(id)listener
{
  NSLog(@"request: %@", request);
  NSLog(@"url: %@", [actionInformation objectForKey: @"WebActionOriginalURLKey"]);

  NSString *WebActionElementKey = @"WebActionElementKey";
  id key;
 
  for (key in actionInformation) {
    NSLog(@"key: %@, value: %@", key, [actionInformation objectForKey:key]);
  }

  if([actionInformation objectForKey: WebActionElementKey] != nil) {
    NSLog(@"loading article with url %@", [request URL]);
    NSLog(@"url path: %@", [[actionInformation objectForKey: @"WebActionOriginalURLKey"] path]);
    NSString *title = [[[[actionInformation objectForKey: @"WebActionOriginalURLKey"] path] substringFromIndex: 1]
                        stringByReplacingPercentEscapesUsingEncoding: NSUTF8StringEncoding];
    [self loadArticle: title];
    [listener use];
  } else
    [listener use];

	NSLog(@"webView:decidePolicyForNavigationAction: %@", [request URL]);
  NSLog(@"listener: %@", listener);
}

- (void) updateHTML: (NSString *) str
{
  [wkv loadString: str];
}

-(void) setDump: (wp_dump *) d {
  dump = d;
}

-(void) notFound: (NSString *) title {
  [self loadArticle: title withContents: [NSString stringWithFormat: @"The article <strong>%@</strong> doesn't exist in this Wikipedia dump.", title]];
}

-(void) loadArticle: (NSString *) title {
  NSString *cap = [NSString stringWithFormat: @"%c%@", toupper([title characterAtIndex: 0]), [title substringFromIndex: 1]];
  NSLog(@"cap: %@", cap);
  if(load_article(dump, [cap UTF8String], article) != -1)
    [self loadArticle: cap withContents: [NSString stringWithUTF8String: article->text]];
  else
    [self notFound: title];
}

-(void) loadArticle: (NSString *) title fromBlock: (int) block {
  block_load_article(dump, [title UTF8String], block, article);
  [self loadArticle: title withContents: [NSString stringWithUTF8String: article->text]];
}

- (void) loadArticle: (NSString *) title withContents: (NSString *) contents {
  WPParser *wp = [[WPParser alloc] initWithMarkup: contents];
  NSString *css = @"body { font-family: Helvetica; width: 310px; padding: 5px; margin: 0; word-wrap: break-word }";
  [self updateHTML: [NSString stringWithFormat: @"<html><head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"><style>%@</style></head><body><h1>%@</h1>%@</body></html>", css, title, [wp parsed]]];
}
@end
