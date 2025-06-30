!/usr/bin/env python3
"""
Test script for the steganography project
Tests various scenarios and edge cases
"""

from main import Steganography
import os

def test_basic_functionality():
    """Test basic hide and extract functionality"""
    print("=== Testing Basic Functionality ===")
    
    stego = Steganography()
    
    # Test message and password
    test_message = "Hello, this is a secret message!"
    test_password = "testpassword123"
    
    # First, create a sample image if it doesn't exist
    if not os.path.exists('sample.png'):
        print("Creating sample image...")
        from generate_sample_image import create_sample_image
        create_sample_image()
    
    # Test embedding
    print("Testing message embedding...")
    success, result = stego.embed_message('sample.png', test_message, test_password, 'test_output.png')
    
    if success:
        print(f"✓ Embedding successful: {result}")
    else:
        print(f"✗ Embedding failed: {result}")
        return False
    
    # Test extraction
    print("Testing message extraction...")
    success, extracted = stego.extract_message('test_output.png', test_password)
    
    if success:
        print(f"✓ Extraction successful: {extracted}")
        if extracted == test_message:
            print("✓ Message integrity verified!")
            return True
        else:
            print("✗ Message integrity check failed!")
            print(f"Expected: {test_message}")
            print(f"Got: {extracted}")
            return False
    else:
        print(f"✗ Extraction failed: {extracted}")
        return False

def test_wrong_password():
    """Test extraction with wrong password"""
    print("\n=== Testing Wrong Password ===")
    
    stego = Steganography()
    
    # Try to extract with wrong password
    success, result = stego.extract_message('test_output.png', 'wrongpassword')
    
    if not success or "Decryption failed" in result:
        print("✓ Wrong password correctly rejected")
        return True
    else:
        print(f"✗ Wrong password was accepted: {result}")
        return False

def test_long_message():
    """Test with a longer message"""
    print("\n=== Testing Long Message ===")
    
    stego = Steganography()
    
    # Create a longer test message
    long_message = "This is a much longer test message that contains multiple sentences. " * 10
    long_message += "We want to test if the steganography system can handle larger amounts of data. "
    long_message += "The message should still be encrypted and embedded properly in the image pixels."
    
    print(f"Message length: {len(long_message)} characters")
    
    # Test embedding
    success, result = stego.embed_message('sample.png', long_message, 'longtest123', 'test_long.png')
    
    if success:
        print("✓ Long message embedding successful")
        
        # Test extraction
        success, extracted = stego.extract_message('test_long.png', 'longtest123')
        
        if success and extracted == long_message:
            print("✓ Long message extraction and verification successful")
            return True
        else:
            print("✗ Long message extraction or verification failed")
            return False
    else:
        print(f"✗ Long message embedding failed: {result}")
        return False

def test_special_characters():
    """Test with special characters"""
    print("\n=== Testing Special Characters ===")
    
    stego = Steganography()
    
    # Message with special characters and emojis
    special_message = "Special chars: !@#$%^&*()_+-=[]{}|;:,.<>? áéíóú ñ 中文 🔐🖼️💾"
    
    # Test embedding
    success, result = stego.embed_message('sample.png', special_message, 'special123', 'test_special.png')
    
    if success:
        print("✓ Special characters embedding successful")
        
        # Test extraction
        success, extracted = stego.extract_message('test_special.png', 'special123')
        
        if success and extracted == special_message:
            print("✓ Special characters extraction and verification successful")
            return True
        else:
            print("✗ Special characters extraction or verification failed")
            print(f"Expected: {special_message}")
            print(f"Got: {extracted}")
            return False
    else:
        print(f"✗ Special characters embedding failed: {result}")
        return False

def test_empty_message():
    """Test with empty message"""
    print("\n=== Testing Empty Message ===")
    
    stego = Steganography()
    
    # Test with empty message
    success, result = stego.embed_message('sample.png', '', 'empty123', 'test_empty.png')
    
    if success:
        print("✓ Empty message embedding successful")
        
        # Test extraction
        success, extracted = stego.extract_message('test_empty.png', 'empty123')
        
        if success and extracted == '':
            print("✓ Empty message extraction and verification successful")
            return True
        else:
            print("✗ Empty message extraction or verification failed")
            return False
    else:
        print(f"✗ Empty message embedding failed: {result}")
        return False

def cleanup_test_files():
    """Clean up test files"""
    test_files = ['test_output.png', 'test_long.png', 'test_special.png', 'test_empty.png']
    
    for file in test_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"Cleaned up {file}")

def main():
    """Run all tests"""
    print("Starting Steganography Tests...")
    print("=" * 50)
    
    tests = [
        test_basic_functionality,
        test_wrong_password,
        test_long_message,
        test_special_characters,
        test_empty_message
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print(f"⚠️ {total - passed} test(s) failed")
    
    # Clean up test files
    print("\nCleaning up test files...")
    cleanup_test_files()
    
    print("Testing completed!")

if __name__ == "__main__":
    main()
