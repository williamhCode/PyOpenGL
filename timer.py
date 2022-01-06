import time

class Timer:
    
    def __init__(self):
        self.time = time.time()
        self.unprocessed = 0
        self.prev_time = time.time()
        self.fps_list = [0]
        
    def tick(self, fps=None):
        if fps != None:
            frame_cap = 1 / fps
            
            while True:
                if self.unprocessed >= frame_cap:
                    self.unprocessed -= frame_cap
                    break
                
                time_2 = time.time()
                self.unprocessed += time_2 - self.time
                self.time = time_2
                
        dt = time.time() - self.prev_time
        self.prev_time = time.time()
        
        if dt != 0:
            self.fps_list.append(1 / dt)
            if len(self.fps_list) > 50:
                self.fps_list.pop(0)
                
        return dt
    
    def get_fps(self):
        return sum(self.fps_list) / len(self.fps_list)