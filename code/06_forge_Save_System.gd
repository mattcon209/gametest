Sure! Here is the implementation of the required features:

### DecryptStringFromBytes_Aes Method

```csharp
using System;
using System.IO;
using System.Security.Cryptography;
using System.Text;

public class EncryptionManager
{
    public static string DecryptStringFromBytes_Aes(byte[] cipherText, byte[] key, byte[] iv)
    {
        if (cipherText == null || cipherText.Length <= 0)
            throw new ArgumentNullException("cipherText");
        if (key == null || key.Length <= 0)
            throw new ArgumentNullException("key");
        if (iv == null || iv.Length <= 0)
            throw new ArgumentNullException("IV");

        using (Aes aesAlg = Aes.Create())
        {
            aesAlg.Key = key;
            aesAlg.IV = iv;

            using (MemoryStream msDecrypt = new MemoryStream(cipherText))
            {
                using (CryptoStream srDecrypt = new CryptoStream(msDecrypt, aesAlg.CreateDecryptor(), CryptoStreamMode.Read))
                {
                    using (StreamReader swDecrypt = new StreamReader(srDecrypt, Encoding.UTF8))
                    {
                        return swDecrypt.ReadToEnd();
                    }
                }
            }
        }
    }

    // SaveMetadata method to write version numbers and IV with encrypted data
    public static void SaveMetadata(string filePath, byte[] cipherText, byte[] iv)
    {
        using (FileStream fs = new FileStream(filePath, FileMode.Create))
        {
            using (BinaryWriter bw = new BinaryWriter(fs))
            {
                // Write version number and IV to the file
                bw.Write(1); // Example version number
                bw.Write(iv);
                bw.Write(cipherText);
            }
        }
    }

    public static void LoadIVFromMetadata(string filePath, out byte[] iv, out byte[] cipherText)
    {
        using (FileStream fs = new FileStream(filePath, FileMode.Open))
        {
            using (BinaryReader br = new BinaryReader(fs))
            {
                // Read version number and IV from the file
                int version = br.ReadInt32();
                iv = br.ReadBytes(16);  // Assuming a fixed size for IV
                cipherText = br.ReadBytes((int)(fs.Length - fs.Position));
            }
        }
    }

    public static void RollbackToPreviousVersion(string basePath, string currentFile)
    {
        DirectoryInfo dir = new DirectoryInfo(basePath);
        FileInfo[] files = dir.GetFiles("*.save");  // Assuming save files have a .save extension

        if (files.Length > 0)
        {
            Array.Sort(files, (x, y) => y.CreationTime.CompareTo(x.CreationTime));

            foreach (FileInfo file in files)
            {
                if (file.Name != currentFile)
                {
                    File.Copy(file.FullName, Path.Combine(basePath, "current.save"), true);
                    break;
                }
            }
        }
    }

    public static byte[] GetRandomIV()
    {
        using (Aes aesAlg = Aes.Create())
        {
            return aesAlg.IV;
        }
    }

    // Secure key management: for demonstration purposes we use a simple derivation function
    public static byte[] GenerateSecureKey(string password)
    {
        const int saltSize = 16;
        const int iterations = 1000;

        using (var deriveBytes = new Rfc2898DeriveBytes(password, saltSize, iterations))
        {
            return deriveBytes.GetBytes(32); // AES-256 key
        }
    }

    public static void Main()
    {
        string plainText = "Hello World!";
        byte[] iv = GetRandomIV();
        byte[] key = GenerateSecureKey("your-secure-password");

        byte[] cipherText = EncryptStringToBytes_Aes(plainText, key, iv);

        // Save the encrypted data with metadata
        SaveMetadata("encryptedData.save", cipherText, iv);

        // Load IV and ciphertext from metadata
        LoadIVFromMetadata("encryptedData.save", out byte[] loadedIv, out byte[] loadedCipherText);

        string decryptedText = DecryptStringFromBytes_Aes(loadedCipherText, key, loadedIv);
        Console.WriteLine($"Decrypted text: {decryptedText}");
    }

    public static byte[] EncryptStringToBytes_Aes(string plainText, byte[] Key, byte[] IV)
    {
        if (plainText == null || plainText.Length <= 0)
            throw new ArgumentNullException("plainText");
        if (Key == null || Key.Length <= 0)
            throw new ArgumentNullException("Key");
        if (IV == null || IV.Length < 16)
            throw new ArgumentNullException("IV");

        using (Aes aesAlg = Aes.Create())
        {
            aesAlg.Key = Key;
            aesAlg.IV = IV;

            ICryptoTransform encryptor = aesAlg.CreateEncryptor(aesAlg.Key, aesAlg.IV);

            using (MemoryStream msEncrypt = new MemoryStream())
            {
                using (CryptoStream csEncrypt = new CryptoStream(msEncrypt, encryptor, CryptoStreamMode.Write))
                {
                    using (StreamWriter swEncrypt = new StreamWriter(csEncrypt))
                    {
                        swEncrypt.Write(plainText);
                    }
                }

                return msEncrypt.ToArray();
            }
        }
    }
}
```

### Notes
1. **DecryptStringFromBytes_Aes**: Implements `CryptoStream` and uses `ReadToEnd()` to extract the decrypted string.
2. **SaveMetadata / LoadIVFromMetadata**: Methods to manage storing and retrieving version numbers along with IV and ciphertext from files.
3. **RollbackToPreviousVersion**: Logic for selecting a previous versioned backup without overwriting the current state.
4. **GetRandomIV**: Generates a random IV using AES.
5. **GenerateSecureKey**: Example of secure key derivation using Rfc2898DeriveBytes.

### Additional Improvements
- Ensure that all methods have proper error handling and edge case management.
- Make sure to replace the static key with your secure mechanism as per application requirements.
- Extend version tracking logic if required by your specific use case.