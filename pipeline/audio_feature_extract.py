import numpy as np
import glob
import ntpath

import os, sys, glob
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from torchvggish.torchvggish import vggish

class AudioFeatureExtractor():
    def __init__(self, audio_list_path = 'data/audios',
                       feature_save_path = 'data/audio_features'):
        self.audio_list_path = audio_list_path
        self.feature_save_path = feature_save_path

    def extract_audio_features(self):
        # Initialise model and download weights
        model_urls = {
            'vggish': 'https://github.com/harritaylor/torchvggish/'
            'releases/download/v0.1/vggish-10086976.pth',
            'pca': 'https://github.com/harritaylor/torchvggish/'
            'releases/download/v0.1/vggish_pca_params-970ea276.pth'
            }
        embedding_model = vggish.VGGish(urls=model_urls, postprocess=False)
        embedding_model.eval()
        audio_list_file_feature = []
        
        for audio_path in self.audio_list_path:
            audio_name = ntpath.basename(audio_path)
            print(audio_name)
            path_save = (os.path.join(self.feature_save_path, audio_name[:-4])+".npy")
            if os.path.exists(path_save):
                audio_list_file_feature.append(path_save)
                continue
        
            # if os.path.exists(os.path.join(self.feature_save_path, audio_name[:-4])+".npy"):
            #     return os.path.join(self.feature_save_path, audio_name[:-4])+".npy"

            embeddings = embedding_model.forward(audio_path)
            np.save(os.path.join(self.feature_save_path, audio_name[:-4]),embeddings.detach().cpu().numpy())
            
            audio_list_file_feature.append(path_save)
        
        return audio_list_file_feature

if __name__ == "__main__":
    audio_path = '/home/www/data/data/saigonmusic/Dev_AI/kiendn/dataset/horror_audio/horror/*.wav'
    feature_save_path = '/home/www/data/data/saigonmusic/Dev_AI/kiendn/dataset/horror_audio/features/horror'
    audio_list_path = glob.glob(audio_path)
    
    a = AudioFeatureExtractor(audio_list_path, feature_save_path=feature_save_path)
    a.extract_audio_features()