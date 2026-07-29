```csharp
using System;
using System.IO;
using System.Security.Cryptography;
using System.Text;
using UnityEngine;

public static class CloudSaveEncryption
{
    private const string EncryptionKey = "Your32ByteLengthKey"; // Replace with your actual 32-byte key

    public static void SaveData(string savePath, byte[] data)
    {
        var encryptedData = Encrypt(data);
        File.WriteAllBytes(savePath, encryptedData);
    }

    public static byte[] LoadData(string savePath)
    {
        var encryptedData = File.ReadAllBytes(savePath);
        return Decrypt(encryptedData);
    }

    private static byte[] Encrypt(byte[] data)
    {
        using (var aes = Aes.Create())
        {
            aes.Key = Encoding.UTF8.GetBytes(EncryptionKey);
            aes.GenerateIV();

            using (var ms = new MemoryStream())
            {
                ms.Write(aes.IV, 0, aes.IV.Length);

                using (var cryptoStream = new CryptoStream(ms, aes.CreateEncryptor(), CryptoStreamMode.Write))
                {
                    cryptoStream.Write(data, 0, data.Length);
                    cryptoStream.Close();
                }

                return ms.ToArray();
            }
        }
    }

    private static byte[] Decrypt(byte[] data)
    {
        using (var aes = Aes.Create())
        {
            var iv = new byte[aes.BlockSize / 8];
            Array.Copy(data, iv, iv.Length);

            aes.Key = Encoding.UTF8.GetBytes(EncryptionKey);
            aes.IV = iv;

            using (var ms = new MemoryStream())
            {
                using (var cryptoStream = new CryptoStream(ms, aes.CreateDecryptor(), CryptoStreamMode.Write))
                {
                    cryptoStream.Write(data, iv.Length, data.Length - iv.Length);
                    cryptoStream.Close();
                }

                return ms.ToArray();
            }
        }
    }
}
```