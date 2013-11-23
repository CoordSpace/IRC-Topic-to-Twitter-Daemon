import unittest, time
from infoextraction import *

# ---- extract() tests ----
class ExtractTests(unittest.TestCase):

	def setUp(self):
		self.info = ExtractInfo()
	
	# reset the extractinfo object to empty
	def tearDown(self):
		self.info = None
	
	def test_extractEmptyTopic(self):
		topic = ""
		
		self.assertTrue(self.info.extract(topic)[0] == [''])
		
	def test_extractSimpleMovieLink(self):
		topic = '  Movie Nite: http://Whatever.com/movie  '
		
		self.assertTrue(self.info.extract(topic)[0] == ['Movie Nite: http://Whatever.com/movie'])
		
	def test_extractComplexMovieLink(self):
		topic = '  Movie Night! www.ustream.tv/channel/dopevision2 | Film: Funny Games (1997)   '
		
		self.assertTrue(self.info.extract(topic)[0] == ['Movie Night! www.ustream.tv/channel/dopevision2 | Film: Funny Games (1997)'])
	
	def test_extractEmpty(self):
		topic = "Streamer: | Game: |"
		
		self.assertTrue(self.info.extract(topic)[0] == ['', ''])
		
	def test_extractNormalTopic(self):
		topic = "Streamer: Qipz | Game: Tony Hawk American Wasteland|"
		
		self.assertTrue(self.info.extract(topic)[0] == ['Qipz', 'Tony Hawk American Wasteland'])
		
	def test_extractNormalTopicNoTrailingBar(self):
		topic = "Streamer: Qipz | Game: Tony Hawk American Wasteland"
		
		self.assertTrue(self.info.extract(topic)[0] == ['Qipz', 'Tony Hawk American Wasteland'])
		
	def test_extractNormalTopicNoStreamer(self):
		topic = "Streamer: | Game: cue"
		
		self.assertTrue(self.info.extract(topic)[0] == ['', 'cue'])
		
	def test_extractNormalTopicNoGame(self):
		topic = "Streamer: Qipz | Game:|"
		
		self.assertTrue(self.info.extract(topic)[0] == ['Qipz', ''])
			
# ---- uniqueTest() tests ----
class UniqueTests(unittest.TestCase):

	def setUp(self):
		self.processor = ExtractInfo()
	
	# reset the extractinfo object to empty
	def tearDown(self):
		self.processor = None
	
	def test_sameTopicSmallDelay(self):
		self.processor.prevInfo = (['S', 'G'], 100)
		
		self.assertFalse( self.processor.uniqueTest( (['S', 'G'], 101) ) )
		
	def test_sameTopicLongDelay(self):
		self.processor.prevInfo = (['S', 'G'], 100)
		
		self.assertFalse( self.processor.uniqueTest( (['S', 'G'], 1000) ) )
		
	def test_diffTopicSmallDelay(self):
		self.processor.prevInfo= (['S', 'G'], 100)
		
		self.assertFalse( self.processor.uniqueTest( (['A', 'F'], 101) ) )
		
	def test_diffTopicLongDelay(self):
		self.processor.prevInfo = (['S', 'G'], 100)
		
		self.assertTrue( self.processor.uniqueTest( (['A', 'F'], 1000) ) )
		
	def test_diffTopicStreamerLongDelay(self):
		self.processor.prevInfo = (['S', 'G'], 100)
		
		self.assertTrue( self.processor.uniqueTest( (['Q', 'G'], 1000) ) )
		
	def test_diffTopicGameLongDelay(self):
		self.processor.prevInfo = (['S', 'G'], 100)
		
		self.assertTrue( self.processor.uniqueTest( (['S', 'B'], 1000) ) )
		
	def test_diffTopicLenLongDelay(self):
		self.processor.prevInfo = (['S', 'G'], 100)
		
		self.assertTrue( self.processor.uniqueTest( (['A'], 1000) ) )
		
	def test_sameMovieLongDelay(self):
		self.processor.prevInfo = (['Jaws'], 100)
		
		self.assertFalse( self.processor.uniqueTest( (['Jaws'], 1000) ) )
	
	def test_diffMovieLongDelay(self):
		self.processor.prevInfo = (['Jaws'], 100)
		
		self.assertTrue( self.processor.uniqueTest( (['Burds'], 1000) ) )
		
	def test_noTopicToMovieLongDelay(self):
		self.processor.prevInfo = ([], 100)
		
		self.assertTrue( self.processor.uniqueTest( (['Burds'], 1000) ) )
		
	def test_noTopicToMovieShortDelay(self):
		self.processor.prevInfo = ([], 100)
		
		self.assertFalse( self.processor.uniqueTest( (['Burds'], 101) ) )
		
	def test_noTopicToGameLongDelay(self):
		self.processor.prevInfo = ([], 100)
		
		self.assertTrue( self.processor.uniqueTest( (['S', 'G'], 1000) ) )
	
# ---- generateMessage() tests ----
class GenerateMessageTests(unittest.TestCase):

	def setUp(self):
		self.processor = ExtractInfo()
	
	# reset the extractinfo object to empty
	def tearDown(self):
		self.processor = None

	def test_noTopicToMovieLongDelay(self):
		self.processor.prevInfo = ([''], 100)
		
		self.assertTrue( self.processor.generateMessage( 'Movietime! linklinklink' ) == 'Movietime! linklinklink')
		
	def test_noTopicToMovieShortDelay(self):
		self.processor.prevInfo = ([''], time.time())
			
		self.assertFalse( self.processor.generateMessage( 'Movietime!' ) == 'Movietime!')
		
	def test_MovieToNoTopicLongDelay(self):
		self.processor.prevInfo = (['Movienight! Hashsds.tv/dfsdf'], 100)
		
		self.assertTrue( self.processor.generateMessage( '' ) == 'No community messages. If only there were streams...')
		
	def test_MovieToNoTopicLongDelay(self):
		self.processor.prevInfo = (['Movienight! Hashsds.tv/dfsdf'], 100)
		
		self.assertTrue( self.processor.generateMessage( 'Streamer: | Game: |' ) == 'Stream over. Thanks for watching everyone!')
		
	def test_MovieToNoTopicShortDelay(self):
		self.processor.prevInfo = (['Movienight! Hashsds.tv/dfsdf'], time.time())
			
		self.assertTrue( self.processor.generateMessage( '' ) == None)
		
	def test_emptyToGameStreamLongDelay(self):
		self.processor.prevInfo = (['',''], 100)
		
		self.assertTrue( self.processor.generateMessage('Streamer: Qipz | Game: THAW | Some other stuff' ) == 'Qipz is playing THAW @ dopelives.com!' )
		
	def test_emptyToGameStreamShortDelay(self):
		self.processor.prevInfo = (['',''], time.time())
			
		self.assertTrue( self.processor.generateMessage( 'Streamer: Qipz | Game: THAW | Some other stuff' ) == None)
		
	def test_emptyToGameStreamNoSecondBarLongDelay(self):
		self.processor.prevInfo = (['',''], 100)
		
		self.assertTrue( self.processor.generateMessage('Streamer: Qipz |Game: THAW ' ) == 'Qipz is playing THAW @ dopelives.com!' )

	def test_emptyToComplexMovieLongDelay(self):
		self.processor.prevInfo = (['',''], 100)
		
		self.assertTrue( self.processor.generateMessage('Movienight! http:fsfkasfka | Movie title | Jimmy- is now banned, nerds  ' ) == 'Movienight! http:fsfkasfka | Movie title | Jimmy- is now banned, nerds' )
		
	def test_gameStreamToNoStreamLongDelay(self):
		self.processor.prevInfo = (['Qipz','THAW'], 100)
		
		self.assertTrue( self.processor.generateMessage('Streamer:  | Game:| Some other stuff' ) == 'Stream over. Thanks for watching everyone!' )
		
	def test_gameStreamToNoStreamShortDelay(self):
		self.processor.prevInfo = (['Qipz','THAW'], time.time())
			
		self.assertTrue( self.processor.generateMessage( 'Streamer:  | Game:| Some other stuff' ) == None)
		
	def test_changeGameLongDelay(self):
		self.processor.prevInfo = (['Qipz','THAW'], 100)
		
		self.assertTrue( self.processor.generateMessage('Streamer: Qipz | Game: PoE | Some other stuff' ) == 'Qipz is playing PoE @ dopelives.com!' )
		
	def test_changeStreamerLongDelay(self):
		self.processor.prevInfo = (['Qpz','THAW'], 100)
		
		self.assertTrue( self.processor.generateMessage('Streamer: Qipz | Game: THAW | Some other stuff' ) == 'Qipz is playing THAW @ dopelives.com!' )
		
	def test_gameToSimpleMovieLongDelay(self):
		self.processor.prevInfo = (['Qpz','THAW'], 100)
		
		self.assertTrue( self.processor.generateMessage('Movienight! http:fsfkasfka' ) == 'Movienight! http:fsfkasfka' )
		
	def test_gameToComplexMovieLongDelay(self):
		self.processor.prevInfo = (['Qpz','THAW'], 100)
		
		self.assertTrue( self.processor.generateMessage('Movienight! http:fsfkasfka | Movie title | Jimmy- is now banned, nerds  ' ) == 'Movienight! http:fsfkasfka | Movie title | Jimmy- is now banned, nerds' )
		
	def test_nothingToNoStreamerLongDelay(self):
		self.processor.prevInfo = (['',''], 100)
		
		self.assertTrue( self.processor.generateMessage('Streamer: | Game: Cue | Dopelives Awards 2013 Nominations: goo.gl/Qa78UH |' ) == '??? is playing Cue @ dopelives.com!' )
		
	def test_nothingToNoGameLongDelay(self):
		self.processor.prevInfo = (['',''], 100)
		
		self.assertTrue( self.processor.generateMessage('Streamer: Qipz | Game: | Dopelives Awards 2013 Nominations: goo.gl/Qa78UH |' ) == 'Qipz is playing ??? @ dopelives.com!' )
		
if __name__ == '__main__':
	unittest.main()
