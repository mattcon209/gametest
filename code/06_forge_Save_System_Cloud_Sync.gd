```csharp
using System;
using UnityEngine;
using UnityEngine.SocialPlatforms;

public class SaveSystem : MonoBehaviour
{
    private const string CloudSaveKey = "BudgetBodyguardsSaveData";
    private string localFilePath;

    void Start()
    {
        localFilePath = Application.persistentDataPath + "/saveGame.json";

#if UNITY_ANDROID && !UNITY_EDITOR
        Social.localUser.Authenticate((bool success) =>
        {
            if (success)
            {
                LoadCloudSaveData();
            }
            else
            {
                Debug.LogWarning("Failed to authenticate with Google Play Games. Falling back to local save.");
                LoadLocalSaveData();
            }
        });
#elif UNITY_IOS && !UNITY_EDITOR
        Social.localUser.Authenticate((bool success) =>
        {
            if (success)
            {
                LoadCloudSaveData();
            }
            else
            {
                Debug.LogWarning("Failed to authenticate with Game Center. Falling back to local save.");
                LoadLocalSaveData();
            }
        });
#else
        LoadLocalSaveData();
#endif
    }

    public void SaveGameData(SaveData data)
    {
#if UNITY_ANDROID && !UNITY_EDITOR || UNITY_IOS && !UNITY_EDITOR
        if (Social.localUser.authenticated)
        {
            Social.SaveCloudSaveData(data, CloudSaveKey, OnCloudSaveSuccess);
        }
#endif
        SaveLocalSaveData(data);
    }

    private void LoadCloudSaveData()
    {
        try
        {
            Social.LoadCloudSaveData(CloudSaveKey, (ICloudSaveData data) =>
            {
                if (data != null && !string.IsNullOrEmpty(data.totalSize))
                {
                    Debug.Log("Cloud save data loaded successfully.");
                    // Process the cloud save data here
                }
                else
                {
                    Debug.LogWarning("Failed to load cloud save data. Falling back to local save.");
                    LoadLocalSaveData();
                }
            });
        }
        catch (Exception e)
        {
            Debug.LogError("Exception when loading cloud save data: " + e.Message);
            LoadLocalSaveData();
        }
    }

    private void SaveLocalSaveData(SaveData data)
    {
        try
        {
            string json = JsonUtility.ToJson(data);
            System.IO.File.WriteAllText(localFilePath, json);
            Debug.Log("Local save data saved successfully.");
        }
        catch (Exception e)
        {
            Debug.LogError("Exception when saving local save data: " + e.Message);
        }
    }

    private void LoadLocalSaveData()
    {
        try
        {
            string json = System.IO.File.ReadAllText(localFilePath);
            SaveData data = JsonUtility.FromJson<SaveData>(json);
            Debug.Log("Local save data loaded successfully.");
            // Process the local save data here
        }
        catch (Exception e)
        {
            Debug.LogError("Exception when loading local save data: " + e.Message);
        }
    }

    private void OnCloudSaveSuccess(bool success, string data)
    {
        if (success)
        {
            try
            {
                SaveData savedData = JsonUtility.FromJson<SaveData>(data);
                // Process the cloud save data here
            }
            catch (Exception e)
            {
                Debug.LogError("Exception when processing cloud save data: " + e.Message);
                LoadLocalSaveData();
            }
        }
    }
}

[Serializable]
public class SaveData
{
    public int score;
    public float timePlayed;
}
```