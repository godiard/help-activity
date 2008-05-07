#import "WPParser.h"

@implementation WPParser 

-(WPParser *) initWithMarkup: (NSString *) markup {
  [self init];
  raw = [[ReadStream alloc] initWithString: markup];
  return self;
}

-(void) parseLink {
  NSString *linkText, *linkHref, *text;
  
  [raw expect: '['];
  [raw expect: '[']; 
  text = [raw readUpto: ']'];
  [raw expect: ']'];
  [raw expect: ']'];

  NSRange range = [text rangeOfString: @"|"];
  if(range.location != NSNotFound) {
    linkText = [text substringFromIndex: range.location + 1];
    linkHref = [text substringToIndex: range.location];
  } else
    linkText = linkHref = text;
  
  [html appendFormat: @"<a href=\"wp://localhost/%@\">%@</a>", linkHref, linkText];
}

-(void) parseHeading {
  NSString *text;

  int level = 0;
  while([raw peek] == '=') { [raw read]; level++; }
  text = [raw readUpto: '='];
  while([raw peek] == '=') [raw read];
    
  [html appendFormat: @"<h%d>%@</h%d>", level, text, level];
} 

-(void) parseItalic {
  if(italic) {
    italic = NO;
    [html appendString: @"</i>"];
  } else {  
    italic = YES;
    [html appendString: @"<i>"];
  } 
}

-(void) parseBold {
  [raw expect: '\''];

  if(bold) {
    bold = NO;
    [html appendString: @"</b>"];
  } else { 
    bold = YES;
    [html appendString: @"<b>"];
  }
}

-(void) parseBoldItalic {
  [raw expect: '\''];
  [raw expect: '\''];

  if([raw peek] == '\'') [self parseBold];
  else [self parseItalic];
}    

-(void) parseTemplateStart {
  [raw expect: '{'];
  [raw expect: '{'];
  tmplLevel++;
}

-(void) parseTemplateEnd {
  [raw expect: '}'];
  [raw expect: '}'];
  tmplLevel--;
}

-(void) parse {
  while(![raw isAtEnd]) {
    unichar c = [raw peek];

    if(c == '{' && [raw peekTwo] == '{') 
      [self parseTemplateStart];
    else if(c == '}' && [raw peekTwo] == '}') 
      [self parseTemplateEnd];
    else if(tmplLevel > 0) 
      [raw read];
    else if(c == '[' && [raw peekTwo] == '[')
      [self parseLink];
    else if ([raw peekBack] == '\n' && [raw peek] == '=')
      [self parseHeading];
    else if(c == '\'' && [raw peekTwo] == '\'')
      [self parseBoldItalic];
    else
      [html appendFormat: @"%c", [raw read]];
  }
}

-(NSString *) parsed {
  html = [[NSMutableString alloc] init];
  bold = NO;
  italic = NO;
  tmplLevel = 0;
  [self parse];
  return html;
}

@end
