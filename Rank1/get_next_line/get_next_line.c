/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   get_next_line.c                                   :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: harnakam <harnakam@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/07/25 14:30:10 by harnakam         #+#    #+#              */
/*   Updated: 2026/07/25 15:05:40 by harnakam        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

char	*get_next_line(int fd)
{
	static char	*stash;
	char		*line;

	if (fd < 0 || BUFFER_SIZE <= 0)
		return (NULL);
	stash = read_to_stash(fd, stash);
	if (stash == NULL)
		return (NULL);
	line = extract_line(stash);
	if (line == NULL)
	{
		free(stash);
		stash = NULL;
		return (NULL);
	}
	stash = keep_rest(stash);
	return (line);
}

char	*read_to_stash(int fd, char *stash)
{
	char	*buffer;
	ssize_t	bytes_read;

	buffer = malloc(BUFFER_SIZE + 1);
	if (buffer == NULL)
		return (NULL);
	bytes_read = 1;
	while (bytes_read > 0 && ft_strchr(stash, SEP) == NULL)
	{
		bytes_read = read(fd, buffer, BUFFER_SIZE);
		if (bytes_read < 0)
		{
			free(buffer);
			free(stash);
			return (NULL);
		}
		buffer[bytes_read] = '\0';
		if (bytes_read > 0)
			stash = ft_strjoin_free(stash, buffer);
	}
	free(buffer);
	return (stash);
}

char	*extract_line(char *stash)
{
	char	*line;
	size_t	i;
	size_t	j;

	if (stash == NULL || stash[0] == '\0')
		return (NULL);
	i = 0;
	while (stash[i] != '\0' && stash[i] != SEP)
		i++;
	if (stash[i] == SEP)
		i++;
	line = malloc(sizeof(char) * (i + 1));
	if (line == NULL)
		return (NULL);
	j = 0;
	while (j < i)
	{
		line[j] = stash[j];
		j++;
	}
	line[j] = '\0';
	return (line);
}

static char	*copy_rest(char *stash, size_t start)
{
	char	*rest;
	size_t	i;

	rest = malloc(ft_strlen(stash + start) + 1);
	if (rest == NULL)
		return (NULL);
	i = 0;
	while (stash[start] != '\0')
		rest[i++] = stash[start++];
	rest[i] = '\0';
	return (rest);
}

char	*keep_rest(char *stash)
{
	char	*rest;
	size_t	i;

	i = 0;
	while (stash[i] != '\0' && stash[i] != SEP)
		i++;
	if (stash[i] == '\0')
	{
		free(stash);
		return (NULL);
	}
	rest = copy_rest(stash, i + 1);
	free(stash);
	if (rest == NULL || rest[0] == '\0')
	{
		free(rest);
		return (NULL);
	}
	return (rest);
}
