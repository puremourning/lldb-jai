DEBUG = 0

import lldb
if DEBUG:
  import debugpy

def String( valobj: lldb.SBValue, internal_dict, options ):
  data: lldb.SBValue = valobj.GetChildMemberWithName('data')
  len = valobj.GetChildMemberWithName('count').GetValueAsSigned(0)
  return bytes( data.GetPointeeData(0, len).uint8s ).decode( 'utf-8' )

# Annoyingly summary strings suppress the printing of the child members by
# default. This is crappy, and means we have to write that code ourselves, but
# it's not even that trivial as just printing the "GetValue()" of each child
# prints "None", helpfully.
def Array( valobj: lldb.SBValue, internal_dict, options ):
  raw: lldb.SBValue = valobj.GetNonSyntheticValue()
  return ( "Array(count="
           + str( raw.GetChildMemberWithName( 'count' ).GetValueAsSigned() )
           + ")" )

def ResizableArray( valobj: lldb.SBValue, internal_dict, options ):
  raw: lldb.SBValue = valobj.GetNonSyntheticValue()
  data = raw.GetChildMemberWithName( 'data' ).GetValueAsSigned()
  if data == 0:
    return ( "Array(uninitialised)" )

  return ( "Array(count="
           + str( raw.GetChildMemberWithName( 'count' ).GetValueAsSigned() )
           + ",allocated="
           + str( raw.GetChildMemberWithName( 'allocated' ).GetValueAsSigned() )
           + ")" )

class ArrayChildrenProvider:
  def __init__( self, valobj: lldb.SBValue, internal_dict) :
    self.val = valobj

  def update(self):
    self.count = self.val.GetChildMemberWithName( 'count' ).GetValueAsSigned()
    self.data: lldb.SBValue = self.val.GetChildMemberWithName('data')
    self.data_type: lldb.SBType = self.data.GetType().GetPointeeType()
    self.data_size = self.data_type.GetByteSize()

    return False

  def has_children(self):
    return True

  def num_children(self):
    return self.count

  def get_child_at_index(self, index):
    return self.data.CreateChildAtOffset( str(index),
                                          self.data_size * index,
                                          self.data_type )

  def get_child_index(self, name):
    return int( name )


def __lldb_init_module( debugger: lldb.SBDebugger, dict ):
  if DEBUG:
    debugpy.listen( 5432 )
    debugpy.wait_for_client()

  cat: lldb.SBTypeCategory = debugger.CreateCategory("Jai")

  string = lldb.SBTypeNameSpecifier( "string" )
  cat.AddTypeSummary( string,
                      lldb.SBTypeSummary.CreateWithFunctionName(
                        'jaitype.String' ) )

  array = lldb.SBTypeNameSpecifier( r'\[\] .*', True )
  cat.AddTypeSummary(
    array,
    lldb.SBTypeSummary.CreateWithFunctionName( 'jaitype.Array' ) )
  cat.AddTypeSynthetic(
    array,
    lldb.SBTypeSynthetic.CreateWithClassName(
      'jaitype.ArrayChildrenProvider' ) )

  rarray = lldb.SBTypeNameSpecifier( r'\[\.\.\] .*', True )
  cat.AddTypeSummary(
    rarray,
    lldb.SBTypeSummary.CreateWithFunctionName( 'jaitype.ResizableArray' ) )
  cat.AddTypeSynthetic(
    rarray,
    lldb.SBTypeSynthetic.CreateWithClassName(
      'jaitype.ArrayChildrenProvider' ) )

  cat.SetEnabled(True)
