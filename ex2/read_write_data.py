import os
import librosa
import numpy as np

LABEL_MAPPING = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}


def load_train_data():
    train_data = []
    train_folder, labels_folder, _ = next(os.walk("train_data"))
    for label_dir in labels_folder:
        abs_path = os.path.join(train_folder, label_dir)
        label = LABEL_MAPPING[label_dir]

        for file_name in os.listdir(abs_path):
            if not file_name.endswith(".wav"):
                continue

            file_path = os.path.join(abs_path, file_name)
            mfcc = perform_mfcc_transform(file_path)
            mfcc = normalize_mfcc(mfcc)
            train_data.append((mfcc, label))

    return train_data


def load_test_data():
    test_data = []
    test_folder = "test_files"
    for file_name in os.listdir(test_folder):

        if not file_name.endswith(".wav"):
            continue

        file_path = os.path.join(test_folder, file_name)
        mfcc = perform_mfcc_transform(file_path)
        mfcc = normalize_mfcc(mfcc)
        test_data.append((file_name, mfcc))

    return test_data


def perform_mfcc_transform(file_path):

    # load frequency features from wav file using librosa
    y, sr = librosa.load(file_path, sr=None)
    mfcc = librosa.feature.mfcc(y=y, sr=sr)

    # transpose mfcc matrix to obey convention:
    # rows are time frames, columns are features

    mfcc = mfcc.transpose()

    return mfcc


def normalize_mfcc(mfcc_matrix):
    features_max = np.max(mfcc_matrix, axis=0)
    features_min = np.min(mfcc_matrix, axis=0)

    return (mfcc_matrix - features_min) / (features_max - features_min)


def write_results(test_names, euc_predictions, dtw_predictions):
    with open("output.txt", "w") as f:
        test_sample_length = len(test_names)
        for i in range(len(test_names)):
            current_test = test_names[i]
            euc_pred = euc_predictions[i]
            dtw_pred = dtw_predictions[i]
            row_data = "{0} - {1} - {2}".format(current_test, euc_pred, dtw_pred)

            if i < test_sample_length-1:
                row_data += "\n"

            f.write(row_data)


def get_accuracy_compared_to_gold(test_names, euc_predictions, dtw_predictions):
    euc_num_correct = 0
    dtw_num_correct = 0
    num_test_files = len(test_names)
    for i in range(num_test_files):
        current_test = test_names[i]
        euc_pred = euc_predictions[i]
        dtw_pred = dtw_predictions[i]
        gold_pred = gold_model_results[current_test]

        if euc_pred == gold_pred:
            euc_num_correct += 1
        if dtw_pred == gold_pred:
            dtw_num_correct += 1

    euc_accuracy = euc_num_correct / num_test_files
    dtw_accuracy = dtw_num_correct / num_test_files

    print("Euclidean distance accuracy is: {0}".format(euc_accuracy))
    print("DTW distance accuracy is: {0}".format(dtw_accuracy))



gold_model_results = {
'c7889cba-a02a-41a5-91b3-8d20ac528d88.wav':4,
'75377101-e448-4be0-b56f-90392e9a0ab4.wav':2,
'ae25b3c2-983c-4398-9fac-2be3ae4bbdb2.wav':0,
'1d12dfcb-a14f-44be-a3b2-007c8d4571bf.wav':2,
'6ca5b636-295d-4edc-8d1d-5c1deacde8d6.wav':4,
'bc89ffa1-d288-455a-a286-c27050354fbf.wav':5,
'268e5239-319f-4535-9c0a-2b2aad718b17.wav':1,
'25284111-7953-475c-a12d-57281df48390.wav':1,
'45699e71-cff7-4792-abd5-9a4fea6b74b7.wav':0,
'5d34c47d-3e41-4fe5-86e2-6e394c7739e1.wav':3,
'028dac84-ab62-4d67-8222-2674ffd94c32.wav':1,
'9325bb5c-886e-4b72-b8cb-29c23aac8e3a.wav':0,
'19159907-1140-4797-b9ef-600d76637ba3.wav':1,
'28e4b97f-0711-48bf-af40-8922c7a255e5.wav':3,
'04499f2a-6764-4347-9f26-0fd7cef37e0c.wav':4,
'f492d24b-31b9-4835-a092-d67c09f83380.wav':2,
'ab6d13a3-6e55-41c5-b403-685a50292032.wav':0,
'1d48533d-b9b9-48c4-a71b-0bc8a23dca76.wav':1,
'a57c14e0-efb1-49fa-bb5b-1d11c543b3b6.wav':1,
'b7fa1e1f-b022-48c7-943a-940020d4cd7b.wav':5,
'9d61b55c-6095-4b88-ad8c-589a5089b7b6.wav':0,
'50dfcdcc-3120-4840-a30c-b5d78ce64a2a.wav':5,
'fdb56edc-2842-4b10-be22-2bb0bcb800a4.wav':3,
'1f6ed61d-9c78-4840-95dd-9f0685eabc87.wav':2,
'4e480e16-41d9-4cb0-b4ed-cf0906fcdc1c.wav':5,
'8286fbba-f4e0-4881-b0e5-9c06622ac7f3.wav':5,
'7ba62ab2-3731-40ad-97d1-465cdc424fc1.wav':1,
'ea37a038-e95f-4326-a888-9948d29bd785.wav':0,
'430b62e2-fe14-4066-bb10-d654f5a79c2f.wav':1,
'8ecfb9b4-3bc5-4847-989f-8148f3bc32ff.wav':1,
'7f5764ba-c02d-4b6e-8286-bb35d7ae59f0.wav':5,
'830f6e35-26ae-4d8d-b63f-1de238ea7d1f.wav':5,
'a8108ba9-66ff-42ba-b6e8-72b3f28bdada.wav':3,
'8dde38e6-bf0a-4dc3-83e4-3833dd9f8b9f.wav':0,
'5bbc873a-b5eb-4ff6-8ce8-f98f7d657374.wav':2,
'00d4b9cd-3619-482a-9941-b5dc2b277cc5.wav':0,
'34651c7c-de01-4a38-82d4-e7a4f45c3a18.wav':1,
'4521b114-1f2c-4f7a-9bf4-724cf6e64d1e.wav':1,
'8a24cb52-ee67-4977-878e-bad289cd89b4.wav':0,
'05557ce9-00e4-4a6a-9ae2-a9f9d4f54778.wav':2,
'599a2dfd-ad00-490f-acda-d6643dace85e.wav':2,
'087c5db0-ae85-412a-9376-fd102fc25325.wav':4,
'3e368f06-dcd2-49d5-a035-d2650a388e8e.wav':1,
'33d036be-0c53-46c3-adb5-a628e2fc407d.wav':4,
'37453fca-861f-4503-b9f6-78586d980068.wav':5,
'd04d3c25-75cc-4ad8-8151-f5201877199c.wav':5,
'1bfb62e9-19e8-47d3-980f-cd97815414cd.wav':2,
'07a03cb0-71a2-49df-be3e-2f12331caf66.wav':0,
'daec9600-cc98-4b2e-9a11-661c2bd98973.wav':0,
'a2b74abd-56a2-4132-a783-03682d6f996f.wav':3,
'c57854eb-eb05-4b42-b3bc-f5ebef6d65bb.wav':0,
'fba325b5-404d-4650-a6c6-7f1d3533091e.wav':4,
'83eeabe0-4b7f-4e79-b2fe-c6e58df6fd1b.wav':5,
'f4ea3cb0-b622-43ab-9cdf-b76d3cb74efd.wav':0,
'8dce6e4b-dff2-4fe8-964c-520d909d6794.wav':0,
'140f2c72-feb7-491b-9f37-b380079d0413.wav':0,
'39e94edc-21d5-4a8b-bd79-642a77d6a29a.wav':1,
'8503ffdb-364a-4357-b3cf-c00b9d3b978c.wav':3,
'664fdc50-4878-4007-9f48-064cb2fb00f3.wav':2,
'9cff19ae-82bf-4724-93b2-8c3c517116bb.wav':1,
'5c615229-487a-4b9a-9f05-dc28862b1080.wav':4,
'213fd769-c85e-49de-9a4e-53040d4413d2.wav':1,
'2dc2e0c7-c37c-438c-8c91-4d0183b73d71.wav':4,
'08fb736c-bd13-4d58-94ee-d474bf6b07d8.wav':3,
'a4db7d82-dcaf-4c5b-8c6e-537d56806713.wav':5,
'cf8d8bfa-50c4-4405-99a9-6874b3afcf82.wav':0,
'b97a5b12-3d4c-4b7b-9e29-f9d193ad63e1.wav':5,
'e0a43e60-caf1-4718-ba05-c17eff75e543.wav':1,
'b2c1cc8a-181a-4597-9a04-db5da4f5eed2.wav':3,
'f5032534-cc6a-4fbe-ad96-1379fdedb0cd.wav':1,
'7928ba57-85b3-4d76-ad3f-ed2732529d6a.wav':0,
'b3e5bd65-ad6c-4e1c-a84e-c70c5243bf71.wav':0,
'31cf92fb-19cc-4a36-bba8-cb5ee04a1a2c.wav':0,
'970fb3a5-607d-400b-a752-78442565d07c.wav':3,
'c8711737-b27d-4da5-9849-cfc091adf542.wav':2,
'd61ba634-f1bb-4655-96b0-6567fec0c7fc.wav':0,
'96995125-00a9-4f5b-91a8-df865b184ca2.wav':0,
'8465cf57-d28a-4877-9380-5fb8124194bc.wav':2,
'6943d745-564c-47c5-8d0a-1586fe7bfcda.wav':0,
'b097b455-ce93-491b-9c35-30b6a6c0f84c.wav':3,
'8430c1a5-3f12-468a-bbc4-b0e6d4c7ae6e.wav':1,
'0598455c-3673-4ca8-88f0-f10defbbbe66.wav':1,
'fc627939-9957-4cfc-a6d7-24773953f60e.wav':0,
'82d86519-264a-4233-875f-99689ce836a9.wav':2,
'c497d9c9-24f8-4e28-b4db-28e74313188c.wav':0,
'5017863d-e41c-4f5d-b911-4c06f309fa1d.wav':5,
'1a853e23-44cd-4534-b454-942e4fbb6fab.wav':0,
'0383c725-7ecb-4ab7-848e-b1350bbaf1e2.wav':5,
'252b660c-8abd-49f7-9f24-864c876b3770.wav':1,
'43e341e3-f9bc-48f6-994b-95f46bbf6606.wav':3,
'127a57be-230a-4bda-bd94-6a2a7899cc67.wav':3,
'28b96479-7c64-4a90-9ed3-c587096ed43e.wav':0,
'8642f265-db70-49eb-bd39-47f79ddec1a5.wav':0,
'11eb6472-cd9f-4f71-9a9c-793a8d8d6cfe.wav':4,
'eb172156-e393-43e9-8f30-0d629b4f900f.wav':2,
'5459f606-ce6b-4e42-b53d-6b1bed6af44d.wav':4,
'f44ea05b-177b-4b65-8c9e-cf77c65de82a.wav':1,
'8ae8eecf-2059-4705-bdce-604acf8d4212.wav':5,
'c28d972d-c0cd-4f2f-9da4-aaf4e91a4d38.wav':2,
'ed971c32-4a3e-4f8a-86fb-f5463e10ddb1.wav':0,
'60177aa3-b10f-477c-8e61-4d29adb0365b.wav':1,
'dec50c0b-a533-439f-982b-3a1d96660b5d.wav':3,
'484b3b57-4a3f-4a8c-83e4-cef15a5caa96.wav':3,
'e80018b3-23d0-4964-be92-a616e0243ce0.wav':1,
'85bfb0d6-b35a-4a86-a18c-ec77b866d5cd.wav':5,
'83afde26-e408-4bb1-90a0-b760d1236445.wav':5,
'1882a912-acfb-4669-a2b5-a26eb1a2560b.wav':4,
'25e0e32b-8931-4073-ab2a-7db41bf020e5.wav':5,
'ba86126c-55df-4eae-9dd5-caf40250bb85.wav':2,
'3440c293-a1f4-4d0f-a816-d1895698bac4.wav':4,
'3503ba57-8466-416f-9138-cbffaf3dd192.wav':0,
'10d650c7-cc46-436d-9162-ad359419e54a.wav':5,
'71cf50d5-4f64-48ab-b73f-d4da46d28ab3.wav':0,
'5777e00d-4860-4376-af61-3599b4fab79d.wav':1,
'de393e7b-4823-42f1-bc68-75855baf6eb3.wav':5,
'41767a19-452b-47b0-8cd1-93dd294f4efc.wav':0,
'967e0002-4a91-4829-9465-671d8621eeaf.wav':3,
'9aa7ac62-88e3-405d-a816-35943656bf2a.wav':2,
'a044b1ed-e35f-45b3-b38e-d953339faf58.wav':2,
'b2113e68-0758-4a12-93e7-67bf7888e2f5.wav':3,
'bac00a60-1666-4a3d-bc18-98c7ef0c8887.wav':5,
'5c89a2e5-b3ae-454a-a46b-c2dd8d85bcd6.wav':5,
'aaa74c5a-c859-459e-96ea-ff4442105b5b.wav':0,
'52372108-2b05-4bfb-94ea-7eaa5cebfd8c.wav':2,
'a01f2620-a92c-497c-8510-3ba5c361fc25.wav':5,
'c874a51f-5aad-4465-8835-6d888a869b45.wav':3,
'e1e881b0-7a76-4084-91de-2b4fa0246231.wav':4,
'3a68494d-b0c5-4e02-9003-dcf5f0625cbc.wav':5,
'8f2cabaf-083f-449c-876e-d0e02d7d57ed.wav':5,
'810147e7-f178-48de-90c6-2bb2699297a6.wav':5,
'b1330bf4-faff-411b-94a0-6a63e0b7ea7a.wav':2,
'a8e4dfe2-ca6e-454a-9b2a-6f7ca0faa651.wav':4,
'dc4427a7-033a-480e-89df-2b7e56093138.wav':0,
'b3554f7e-64cf-46d9-b0ed-c1592dab1c33.wav':0,
'e154ea73-8002-4c6f-9c4b-ed386a6ac415.wav':0,
'5d05f2ba-ba1b-4697-beba-8fc3fd64c136.wav':2,
'0c01329d-f96c-4de2-86b9-430b19e3f112.wav':2,
'd02812d3-5ebf-466e-b4bb-8f0fa13a0a90.wav':5,
'fdb31f76-2f16-4f29-80cb-d24f30e94020.wav':1,
'c549d2a1-e1d2-443c-8300-8b1a56ad3162.wav':4,
'4fe8949e-731b-4725-b166-0aa856040a43.wav':4,
'e638c2cf-726d-4fca-b620-1a6e87213dee.wav':3,
'c9cb601d-1db5-4c1a-bc4e-7e3d17fe5e6c.wav':4,
'6220a048-10ae-4960-97c0-c391b52094ef.wav':5,
'62692252-9dd4-4c64-9fe0-791091d8e7b5.wav':2,
'1ea6996f-ab27-43d6-8716-00912cb6ab48.wav':3,
'81691ad0-894d-40d1-b910-1407cf965236.wav':3,
'e147f052-d493-40b5-8e28-eb103e5fd77f.wav':0,
'7fbe2ce6-c7ef-40e7-a233-5096ddf3b261.wav':3,
'725baf09-6f3f-4d5a-82ac-df5b25474701.wav':3,
'64e03246-894a-4590-9dcd-a53daed26289.wav':1,
'350d9b09-9933-4b6b-afdb-eeb01173f83f.wav':4,
'31064e00-caff-4d15-ade3-c0a77cf18f5f.wav':5,
'405848c6-9ec3-4d5c-9aa7-73f492b9b493.wav':4,
'a53eaad1-54d2-42e3-af01-986e9c56c3aa.wav':0,
'b9433593-d410-457e-98b8-0274ae7e3729.wav':5,
'3161022d-1e2d-4ad8-8358-e92381c8f8c2.wav':0,
'd935b9b7-92d2-4be0-86dd-f3d7df5ea76a.wav':5,
'985745e4-ec91-4722-b3a2-91fbeb81447b.wav':0,
'41662836-30f1-40bf-8d4a-b88373b4d8c5.wav':1,
'837ddba7-beb1-47eb-92ac-23f8b522534c.wav':0,
'00db2adf-d3e7-4106-89af-30d6284ee8fb.wav':0,
'8be57bf0-b1be-414e-87f7-be4b3fc5716d.wav':0,
'08c9696f-6074-4b58-baa4-013383905dd2.wav':0,
'61632aa6-d61d-4c0c-9b20-4b4fc2c7d9aa.wav':3,
'b96fad77-89ea-4ce0-be29-1df9c5eea394.wav':0,
'646407ad-7ef5-4e00-9b8c-7155acd697df.wav':4,
'ea0949d7-737c-4714-a634-ccffa8b586f8.wav':2,
'80a9291a-cae4-475d-96dd-49e4f71fa562.wav':3,
'13be6139-d0c4-4b15-86da-b6eb84fc6ca8.wav':4,
'c8bf68fb-fd34-46b6-a990-eab5a98b5d8b.wav':2,
'790f4165-98cb-43a3-8951-f846910ca278.wav':4,
'ca1b05c3-ee4a-4e4c-9083-a3bc4f343748.wav':4,
'7234fc6f-c86b-43c9-9034-d23bd99d0a60.wav':0,
'e8d8fab9-ac07-47fc-9c47-317129023acb.wav':1,
'd0849f0e-5978-4927-b14b-9b91f94292a9.wav':1,
'84c0421d-5dec-4a5e-ad45-190542689e38.wav':0,
'de229cc4-2fce-4311-9221-e2567278c9df.wav':0,
'bf444e81-9ea2-4797-8338-7fd4af02e592.wav':3,
'382621c6-bdd8-49f1-9abb-1b7248806e2c.wav':0,
'b89006f9-cfa8-4564-8be2-ffc4350a3b71.wav':3,
'3edab843-4738-4b2c-9f8b-ffda294bfb74.wav':4,
'afb35b5f-c1f1-499a-98a2-8eaf5ae8e997.wav':3,
'959cb630-0157-4024-a704-6717755cc772.wav':1,
'518c6735-3750-4fe4-8d10-4f8718c7a78b.wav':3,
'bdc21308-5e1c-4dbd-9ebc-b31884905f3d.wav':0,
'172ff334-4f06-48bc-93a4-21645d978ed5.wav':4,
'a1e80e93-12cb-4c75-a77d-9098b9f61435.wav':5,
'b97e72c6-80f5-47ff-addf-f3e54f03950b.wav':3,
'9d7d47b8-ae50-4afa-b70a-3abaa10e8cac.wav':2,
'c8fc1f92-8b82-4f33-8028-84df71fafb90.wav':0,
'b940b379-de79-408c-9040-35b5f9d40a2e.wav':4,
'ea0e7d98-cb6f-45a7-b6ea-92e0000a2a44.wav':0,
'53be1bf7-1cf5-4acb-97f6-608a2a07ff30.wav':3,
'5076c128-19f6-44d0-8ebb-bd83bf14546d.wav':5,
'4d2de19f-c357-4c92-9f22-c395e129d025.wav':3,
'a67f4f2f-5c04-44fe-a092-20874dbf9801.wav':1,
'0cb1d694-8f61-4f0f-8e4d-541a0bdafc1f.wav':2,
'9048c1bd-afbf-457c-85a7-1c45efe38e75.wav':0,
'1ad98aba-4638-4245-ac36-88d109550adf.wav':2,
'75febe8c-8a8d-4a0f-aa99-2d840550200e.wav':0,
'4e567d19-d430-4d7a-a4dd-dc9191cd3567.wav':0,
'e615f06f-b7fd-4537-a4da-de789e5d0feb.wav':0,
'7cee59f7-c779-458e-b624-6aa26ad2aaee.wav':2,
'88b123d6-c2d3-411b-9384-a35d0ea5e843.wav':0,
'cf332be6-94e1-4cb1-9920-c048992229e6.wav':5,
'1c08381b-e6e9-427d-b221-8bdde5ce4530.wav':3,
'c94421a1-5f7d-42e4-a5fd-67c588bbeaa8.wav':1,
'006e8725-6756-4485-a7be-174ce20c9c54.wav':4,
'c5be4b3d-94ce-4a14-9f80-9db95a1df6fa.wav':5,
'5fda692c-5c07-4771-a471-a7c5cf974f29.wav':1,
'9fa65f8e-13ba-4957-8b31-b5994e4ab0b2.wav':2,
'cdae5fb4-2b78-4639-a351-64f25fcb12c7.wav':5,
'fbb2e629-b1b0-4b93-893e-55b3b5dd7304.wav':0,
'46dc3191-5974-41bc-93a5-e511d36938b7.wav':1,
'0830c20b-eae2-44d1-be89-2efc89c2cce5.wav':4,
'ebdc6a9b-328f-47b8-a369-d779a5bf7bb9.wav':4,
'b7f8e2f2-1442-46c4-a45f-9b5bacfce621.wav':2,
'2c9f70ef-331c-4ed3-8299-fc4ed97d2b04.wav':5,
'b995aa57-5639-4ccd-873d-18d76b9e8e4a.wav':4,
'997cb9ab-3370-4dfa-876c-331ac129df1a.wav':4,
'3adc838b-c6d3-4ce3-83c9-a6d47ba92fbe.wav':4,
'c9f7c690-1844-4b9c-aa2d-14e155bc2765.wav':3,
'795437ff-1bbf-439f-9521-dfd996569322.wav':3,
'1f9ac4cc-f6e6-48e8-87b4-cc1fd51c7ff4.wav':4,
'b2203418-da5e-43b3-946f-75cd0b090113.wav':0,
'211c5507-57e4-4f2d-878e-d2ec64a08060.wav':1,
'94221419-787c-462e-a811-9d42526aaded.wav':2,
'b906bfeb-19c2-4af6-a337-b85924d35607.wav':2,
'ecf82db6-ac99-4b2d-81bf-6ee58fd88d95.wav':2,
'eedcf0f2-c14f-45d6-bb18-2cf9e14c38c8.wav':5,
'9e827628-408b-4111-a180-84449cd0342b.wav':4,
'2baab7c1-7d44-441a-8f76-af3314f46b45.wav':1,
'8b7dc38b-8d9a-435c-8d45-ff44c75bf139.wav':3,
'106822c3-4dc6-4f64-9718-a606e8cd47ed.wav':1,
'70936143-2933-4a55-a2db-a892db793ce0.wav':1,
'5b2e5fb5-8e4d-4b22-b936-d248fc9ca77f.wav':1,
'7df0839c-f3de-47fc-b7a7-80a2ccd14e22.wav':0,
'fb95fddb-c204-4a9f-925c-280f6c332673.wav':2,
'b6eee622-2987-4bd8-bf13-a95d476c4e75.wav':1,
'be7a3807-79a9-41e8-ab0f-9f608374c47b.wav':4,
'39b84103-e939-4ce4-b53c-12b07905c7d0.wav':0,
'2a58b59a-bc06-440f-85fd-6adf5bd3b94a.wav':0,
'8645b6e5-06f8-450a-8039-a7cd207f7e08.wav':4,
'319422b1-4737-49ea-914e-a84711bbf1f4.wav':3,
'a5ea540d-8733-4a18-b2db-1de64770c2df.wav':4,
'c34af20a-1f1c-4e20-adfc-e52ce90704d0.wav':5,
'7135c55c-2d64-4cea-90f1-15b5494fbab3.wav':1,
'eb2f7016-cd34-4b99-b17b-355683780305.wav':0,
'8c2a64fc-ba2a-4309-9cff-4f0f9c0935e9.wav':0
}