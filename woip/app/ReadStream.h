#import <Foundation/Foundation.h>

@interface ReadStream : NSObject {
  NSString *str;
  int pos;
}

-(ReadStream *) initWithString: (NSString *) str;
-(unichar) peek;
-(unichar) peekTwo;
-(unichar) read;
-(unichar) expect: (unichar) c;
-(BOOL) isAtEnd;
-(NSString *) readUpto: (unichar) c;

@end
